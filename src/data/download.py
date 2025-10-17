from __future__ import annotations
import os
from pathlib import Path
import urllib.request

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    url = os.getenv("DATA_URL")
    if not url:
        print(
            "DATA_URL not set. Skip download. Place your CSV into data/raw/ manually."
        )
        return
    dest = RAW_DIR / "dataset.csv"
    print(f"Downloading {url} -> {dest}")
    try:
        urllib.request.urlretrieve(url, dest)
        print("Download complete.")
    except Exception as e:
        print(f"Failed to download: {e}")


if __name__ == "__main__":
    main()
