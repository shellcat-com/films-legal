# -*- coding: utf-8 -*-
"""
update-llms-guides.py: rewrite the Journal guide sections of /llms.txt from
journal-src/meta/*.json (idempotent; edits only the block between the markers).

    python3 scripts/update-llms-guides.py
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://getfilmsera.cam"
SECTIONS = [("Weddings", "Wedding guides"), ("Slideshows", "Slideshow and recap guides"),
            ("Parties", "Party and holiday guides"), ("Photo Sharing", "Photo-sharing guides"),
            ("The Craft", "Film-look guides")]


def main():
    metas = [json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(os.path.join(ROOT, "journal-src", "meta", "*.json")))]
    blocks = []
    for cat, heading in SECTIONS:
        lines = [f"- [{m['title']}]({BASE}/blog/{m['slug']}.html): {m['dek'].rstrip('.')}."
                 for m in metas if m["cat"] == cat]
        if lines:
            blocks.append(f"## {heading}\n" + "\n".join(lines))
    section = "<!-- guides:start -->\n" + "\n\n".join(blocks) + "\n<!-- guides:end -->"
    path = os.path.join(ROOT, "llms.txt")
    s = open(path, encoding="utf-8").read()
    if "<!-- guides:start -->" in s:
        s = re.sub(r"<!-- guides:start -->.*?<!-- guides:end -->", lambda _: section, s, flags=re.S)
    else:
        s = s.replace("\n## Policies", "\n" + section + "\n\n## Policies", 1)
    open(path, "w", encoding="utf-8").write(s)
    print(f"llms.txt: {sum(len(b.splitlines()) - 1 for b in blocks)} guide links in {len(blocks)} sections")


if __name__ == "__main__":
    main()
