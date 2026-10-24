#!/usr/bin/env python3
"""Replace Prophetic Scroll paragraphs from the approved numbered DOCX transcription.
Existing per-document fields and manifest keys are retained.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "migration/scrolls_reviewed_paragraphs.json"
MANIFEST = ROOT / "manifests/prophetic-scrolls.json"
source = json.loads(SOURCE.read_text(encoding="utf-8"))
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
documents = source["documents"]
manifest_by_id = {d["id"]: d for d in manifest["documents"]}
assert len(documents) == len(manifest_by_id) == 325
assert sum(len(d["paragraphs"]) for d in documents) == 2231
seen = set()
changes = []
for item in documents:
    ident = item["id"]
    assert ident not in seen and ident in manifest_by_id
    seen.add(ident)
    path = ROOT / "content/prophetic-scrolls" / (ident + ".json")
    assert path.is_file(), path
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["id"] == ident
    assert record["collection"] == "prophetic-scrolls"
    assert record["scroll_number"] == item["scroll_number"]
    assert record.get("part") == item["part"]
    assert all(b["type"] == "paragraph" for b in record["blocks"]), ident
    paras = item["paragraphs"]
    for index, para in enumerate(paras, start=1):
        assert isinstance(para, str) and "\n" not in para and "\r" not in para and "\t" not in para, (ident, index)
        assert para.startswith(str(index) + ". "), (ident, index)
        assert len(para) > len(str(index)) + 2
    old_keys = set(record)
    record["blocks"] = [
        {"id": "p" + str(i).zfill(3), "type": "paragraph", "text": text}
        for i, text in enumerate(paras, start=1)
    ]
    assert set(record) == old_keys
    new_text = json.dumps(record, ensure_ascii=False, indent=2) + "\n"
    encoded = new_text.encode("utf-8")
    path.write_bytes(encoded)
    manifest_item = manifest_by_id[ident]
    assert manifest_item["number"] == item["scroll_number"]
    assert manifest_item["part"] == item["part"]
    assert manifest_item["json"] == ident + ".json"
    manifest_item["assets"]["json"]["size_bytes"] = len(encoded)
    manifest_item["assets"]["json"]["sha256"] = hashlib.sha256(encoded).hexdigest()
    changes.append({"id": ident, "paragraphs": len(paras), "bytes": len(encoded)})
assert set(manifest_by_id) == seen
MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for item in changes:
    p = ROOT / "content/prophetic-scrolls" / (item["id"] + ".json")
    rec = json.loads(p.read_text(encoding="utf-8"))
    meta = manifest_by_id[item["id"]]["assets"]["json"]
    raw = p.read_bytes()
    assert len(raw) == meta["size_bytes"]
    assert hashlib.sha256(raw).hexdigest() == meta["sha256"]
    assert len(rec["blocks"]) == item["paragraphs"]
    assert all("\n" not in b["text"] and "\r" not in b["text"] for b in rec["blocks"])
status = {
    "status": "PASS",
    "source": source["source"],
    "documents": len(changes),
    "numbered_paragraphs": sum(c["paragraphs"] for c in changes),
    "linebreaks_inside_text": 0,
    "json_schema_fields_preserved": True,
    "manifest_json_hashes_verified": True,
    "note": "Structural/content-transfer verification; not a fresh word-by-word OCR review against the scans."
}
(ROOT / "migration/scrolls_replacement_status.json").write_text(
    json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(status))
