import json
import random
from pathlib import Path

import h5py
import numpy as np
from PIL import Image

BASE = Path(r"D:\adherence_OFM\data\2026_4_22_clonky_a_test_mereni")
SOURCES = ["semgentace_LM5", "semgentace_PC3"]
OUT_DIR = BASE / "segmetnace_labeling_small"
MAPPING_FILE = OUT_DIR / "mapping.json"
SEED = 43
CROPS_PER_IMAGE = 3
CROP_SIZE = 360


def load_image(h5_path: Path) -> np.ndarray:
    with h5py.File(h5_path, "r") as f:
        data = f["images/data"][...]
    return data[0] if data.ndim == 4 else data


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.png"):
        old.unlink()
    if MAPPING_FILE.exists():
        MAPPING_FILE.unlink()

    rng = random.Random(SEED)
    crops: list[tuple[np.ndarray, dict]] = []

    for src in SOURCES:
        snap_dir = BASE / src / "snapshots"
        if not snap_dir.is_dir():
            print(f"skip missing: {snap_dir}")
            continue
        for h5_file in sorted(snap_dir.glob("*.h5")):
            img = load_image(h5_file)
            h, w = img.shape[:2]
            if h < CROP_SIZE or w < CROP_SIZE:
                raise ValueError(
                    f"{h5_file.name}: image {h}x{w} smaller than crop {CROP_SIZE}"
                )
            ch = cw = CROP_SIZE
            rel = h5_file.relative_to(BASE).as_posix()
            for k in range(CROPS_PER_IMAGE):
                y = rng.randint(0, h - ch)
                x = rng.randint(0, w - cw)
                patch = np.ascontiguousarray(img[y : y + ch, x : x + cw])
                crops.append(
                    (
                        patch,
                        {
                            "source": src,
                            "original": rel,
                            "crop_idx": k,
                            "y": y,
                            "x": x,
                            "h": ch,
                            "w": cw,
                            "image_h": h,
                            "image_w": w,
                        },
                    )
                )

    rng.shuffle(crops)

    width = len(str(len(crops)))
    mapping = {}
    for idx, (patch, meta) in enumerate(crops):
        new_name = f"crop_{idx:0{width}d}.png"
        Image.fromarray(patch).save(OUT_DIR / new_name)
        mapping[new_name] = meta
        print(f"{meta['source']}/{Path(meta['original']).name}#{meta['crop_idx']} -> {new_name}")

    with MAPPING_FILE.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "seed": SEED,
                "crops_per_image": CROPS_PER_IMAGE,
                "crop_size": CROP_SIZE,
                "base_dir": str(BASE),
                "files": mapping,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"mapping written: {MAPPING_FILE}")


if __name__ == "__main__":
    main()
