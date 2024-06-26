import argparse
import fnmatch
import gzip
import os
import re
from urllib.parse import urlparse

from cachemoney.simplefile import parse_simplefile


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-dir", "-i", required=True)
    ap.add_argument("--output-root", "-o", default="files", help="output root directory (if not set, no files are written)")
    ap.add_argument("--filter", "-f", help="filter wildcard pattern (e.g. *jpg)")
    ap.add_argument("--decompress", "-d", action="store_true", default=True, help="automatically gunzip")
    args = ap.parse_args()
    output_root = args.output_root
    cache_dir = os.path.abspath(os.path.expanduser(args.cache_dir))
    cache_files = [
        filename
        for filename in os.listdir(cache_dir)
        if re.match("^[0-9a-f]+_0$", filename)
    ]
    for filename in cache_files:
        file = os.path.join(cache_dir, filename)
        with open(file, "rb") as f:
            key, data = parse_simplefile(f)
        if args.filter and not fnmatch.fnmatch(key, args.filter):
            continue
        print(filename, "->", key)
        if output_root:
            url = urlparse(key)
            output_path = os.path.join(output_root, url.netloc, url.path.lstrip("/"))
            if output_path[-1] == '/' or os.path.isdir(output_path):
                continue
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            if args.decompress:
                try:
                    orig_len = len(data)
                    data = gzip.decompress(data)
                    print("  .. decompressed from", orig_len, "to", len(data))
                except Exception:
                    pass
            with open(output_path, "wb") as outf:
                outf.write(data)
            print("  ->", output_path)
            stat = os.stat(file)
            os.utime(output_path, (stat.st_atime, stat.st_mtime))


if __name__ == "__main__":
    main()
