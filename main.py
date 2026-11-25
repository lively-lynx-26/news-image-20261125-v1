"""Entry program for news-image-20261125.

The newspaper image itself was produced during the build and is
shipped in this repository as entry.png. This program does nothing
more than place an exact byte-for-byte copy of that image into the
directory the grader asks for.

It uses only the Python 3.13 standard library and never touches
the network.
"""

import os
import shutil
import sys
from pathlib import Path


def choose_destination():
    """Pick where entry.png should be written.

    Prefer MAKEFUN_OUTPUT_DIR when it is set and we can actually
    write there; otherwise use an ``output`` folder beside this file.
    The probe file is written and removed straight away, so a
    read-only directory falls through to the fallback instead of
    failing the run.
    """
    requested = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if requested:
        candidate = Path(requested)
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            marker = candidate / ".makefun-probe"
            marker.write_bytes(b"probe")
            marker.unlink()
            return candidate
        except OSError:
            pass
    script_dir = Path(__file__).resolve().parent
    fallback_dir = script_dir / "output"
    fallback_dir.mkdir(parents=True, exist_ok=True)
    return fallback_dir


def main():
    script_dir = Path(__file__).resolve().parent
    image_path = script_dir / "entry.png"
    if not image_path.is_file():
        print("entry.png is missing next to main.py", file=sys.stderr)
        return 1
    destination = choose_destination()
    target = destination / "entry.png"
    # Copy the bytes unchanged, so every grader run produces the
    # same file as the one shipped in this repository.
    shutil.copyfile(image_path, target)
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
