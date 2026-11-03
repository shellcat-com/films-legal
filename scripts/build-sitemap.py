# -*- coding: utf-8 -*-
"""
build-sitemap.py: regenerate sitemap.xml from the HTML files in this checkout.

    python3 scripts/build-sitemap.py

- lastmod = the date of the last git commit that touched the file; files with
  uncommitted changes (or never committed) get today's date.
- Skips pages marked noindex, join.html, 404.html, open/, _next/, site/,
  journal-src/, worker/ and node_modules.
- Directory index pages are listed with a trailing slash (/weddings/).
"""

import datetime
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://getfilmsera.cam"
SKIP_DIRS = {"_next", "site", "journal-src", "worker", "node_modules", "open", "docs",
             "marketing", "scripts", "brand", "shots", "assets", ".git", ".well-known", ".preview"}
SKIP_FILES = {"join.html", "404.html", "unsubscribe.html"}
TODAY = datetime.date.today().isoformat()


def git_date(rel):
    dirty = subprocess.run(["git", "status", "--porcelain", "--", rel], cwd=ROOT,
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        return TODAY
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    return out or TODAY


def url_for(rel):
    if rel == "index.html":
        return f"{BASE}/"
    if rel.endswith("/index.html"):
        return f"{BASE}/{rel[:-len('index.html')]}"
    return f"{BASE}/{rel}"


def main():
    entries = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = os.path.relpath(dirpath, ROOT)
        top = rel_dir.split(os.sep)[0]
        if top in SKIP_DIRS:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html") or fn in SKIP_FILES:
                continue
            rel = os.path.normpath(os.path.join(rel_dir, fn)).replace(os.sep, "/")
            with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
                head = f.read(6000)
            if re.search(r'<meta[^>]+name="robots"[^>]+noindex', head):
                continue
            entries.append((url_for(rel), git_date(rel)))
    entries.sort(key=lambda e: (e[0].count("/"), e[0]))
    entries.sort(key=lambda e: e[0] != f"{BASE}/")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lines += [f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>" for u, d in entries]
    lines.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"sitemap.xml: {len(entries)} URLs")


if __name__ == "__main__":
    main()
