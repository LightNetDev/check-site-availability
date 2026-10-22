"""Local HTTP fixtures for the composite action's integration tests."""

import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import time


LOG_LOCK = threading.Lock()
LARGE_SIZE = 8 * 1024 * 1024


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent / "fixtures"), **kwargs)

    def do_HEAD(self):
        if self.path.startswith("/probe/"):
            self.send_response(200)
            self.end_headers()
            self.record(0)
        else:
            super().do_HEAD()

    def record(self, sent):
        with LOG_LOCK:
            with open(self.server.audit_path, "a") as audit:
                audit.write(json.dumps({
                    "method": self.command,
                    "path": self.path,
                    "range": self.headers.get("Range"),
                    "sent": sent,
                }) + "\n")

    def do_GET(self):
        if not self.path.startswith("/probe/"):
            return super().do_GET()
        case = self.path.removeprefix("/probe/")
        sent = 0
        try:
            if case == "range":
                if self.headers.get("Range") != "bytes=0-1023":
                    self.send_error(400)
                    return
                body = b"r" * 1024
                self.send_response(206)
                self.send_header("Content-Range", "bytes 0-1023/8192")
            elif case == "large":
                self.send_response(200)
                self.send_header("Content-Length", str(LARGE_SIZE))
                self.end_headers()
                for _ in range(LARGE_SIZE // 4096):
                    self.wfile.write(b"x" * 4096)
                    self.wfile.flush()
                    sent += 4096
                    time.sleep(0.002)
                return
            elif case == "redirect":
                self.send_response(302)
                self.send_header("Location", "/probe/range")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            elif case == "terminal-redirect":
                self.send_response(302)
                body = b""
            elif case == "empty":
                self.send_response(200)
                body = b""
            elif case == "no-content":
                self.send_response(204)
                body = b""
            elif case == "head-get-fail":
                self.send_response(403)
                body = b"GET is forbidden"
            elif case == "missing":
                self.send_response(404)
                body = b"Not found"
            elif case == "truncated":
                self.send_response(200)
                self.send_header("Content-Length", "1024")
                self.end_headers()
                self.wfile.write(b"incomplete")
                sent = len(b"incomplete")
                self.close_connection = True
                return
            elif case == "binary":
                self.send_response(200)
                body = b"\x00\xff\x00\x01"
            elif case == "short":
                self.send_response(200)
                body = b"Range ignored, but content is available."
            else:
                self.send_response(404)
                body = b"Unknown fixture"
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            sent = len(body)
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            self.record(sent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8123)
    parser.add_argument("--audit", required=True)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.audit_path = args.audit
    server.serve_forever()
