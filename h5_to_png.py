import json
import random
from pathlib import Path

import h5py
import numpy as np
from PIL import Image

BASE = Path(r"D:\adherence_OFM\data\2026_4_22_clonky_a_test_mereni")
SOURCES = ["semgentace_LM5", "semgentace_PC3"]
OUT_DIR = BASE / "segmetnace_labeling"
MAPPING_FILE = OUT_DIR / "mapping.json"
SEED = 42


def convert(h5_path: Path, out_path: Path) -> dict:
    with h5py.File(h5_path, "r") as f:
        data = f["images/data"][...]
        rotation = int(f.attrs.get("rotation", 0))
        mirror = str(f.attrs.get("mirror", ""))

    img = data[0] if data.ndim == 4 else data
    Image.fromarray(np.ascontiguousarray(img)).save(out_path)
    return {"rotation": rotation, "mirror": mirror}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for old in OUT_DIR.glob("*.png"):
        old.unlink()
    if MAPPING_FILE.exists():
        MAPPING_FILE.unlink()

    entries: list[tuple[str, Path]] = []
    for src in SOURCES:
        snap_dir = BASE / src / "snapshots"
        if not snap_dir.is_dir():
            print(f"skip missing: {snap_dir}")
            continue
        for h5_file in sorted(snap_dir.glob("*.h5")):
            entries.append((src, h5_file))

    rng = random.Random(SEED)
    rng.shuffle(entries)

    width = len(str(len(entries)))
    mapping = {}
    for idx, (src, h5_file) in enumerate(entries):
        new_name = f"img_{idx:0{width}d}.png"
        out = OUT_DIR / new_name
        meta = convert(h5_file, out)
        rel = h5_file.relative_to(BASE).as_posix()
        mapping[new_name] = {"source": src, "original": rel, **meta}
        print(f"{src}/{h5_file.name} -> {new_name}")

    with MAPPING_FILE.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "seed": SEED,
                "base_dir": str(BASE),
                "note": (
                    "Snapshots store images with rotation/mirror already "
                    "baked into pixels (see recorder.py:_apply_transform "
                    "called before write). Attributes are kept here as a "
                    "record only; no transform is applied during PNG export."
                ),
                "files": mapping,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"mapping written: {MAPPING_FILE}")


if __name__ == "__main__":
    main()
