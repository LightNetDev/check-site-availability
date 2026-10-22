"""Assert request semantics and early cancellation using fixture server records."""

import json
from pathlib import Path
import sys
import time

case, audit_path = sys.argv[1:]
if case == "connection-failure":
    sys.exit(0)

# A streaming handler can take a moment to observe the client disconnect.
records = []
for _ in range(100):
    if Path(audit_path).exists():
        records = [json.loads(line) for line in Path(audit_path).read_text().splitlines()]
    if any(record["path"] == f"/probe/{case}" for record in records):
        break
    time.sleep(0.01)
else:
    raise AssertionError(f"No request recorded for {case}")

for record in records:
    assert record["method"] == "GET", record
    assert record["range"] == "bytes=0-1023", record
    if record["path"] == "/probe/large":
        assert 0 < record["sent"] < 8 * 1024 * 1024, record
if case == "redirect":
    assert any(record["path"] == "/probe/range" for record in records), records
print(f"Request assertions passed for {case}")
