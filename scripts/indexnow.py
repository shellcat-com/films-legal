# -*- coding: utf-8 -*-
"""
indexnow.py: tell IndexNow search engines (Bing, Yandex, Seznam, Naver, Yep) about
new or changed pages. Google does not use IndexNow; use Search Console for Google.

    python3 scripts/indexnow.py --all            # every URL in sitemap.xml
    python3 scripts/indexnow.py URL [URL ...]    # specific pages

Run only AFTER the pages are live. The key file (<key>.txt at the site root) must be
reachable at https://getfilmsera.cam/<key>.txt, or the submission is rejected.
"""
import glob
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "getfilmsera.cam"


def key():
    for path in glob.glob(os.path.join(ROOT, "*.txt")):
        name = os.path.basename(path)[:-4]
        if re.fullmatch(r"[0-9a-f]{32}", name):
            with open(path) as f:
                if f.read().strip() == name:
                    return name
    sys.exit("No IndexNow key file (<32 hex>.txt containing its own name) at the repo root.")


def sitemap_urls():
    with open(os.path.join(ROOT, "sitemap.xml")) as f:
        return re.findall(r"<loc>([^<]+)</loc>", f.read())


def main(argv):
    urls = sitemap_urls() if argv == ["--all"] else argv
    if not urls:
        sys.exit(__doc__)
    k = key()
    body = json.dumps({"host": HOST, "key": k, "keyLocation": f"https://{HOST}/{k}.txt",
                       "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow: HTTP {r.status} for {len(urls)} URLs")
    except urllib.error.HTTPError as e:
        print(f"IndexNow: HTTP {e.code} {e.reason}: {e.read().decode(errors='replace')[:300]}")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
