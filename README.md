# adherence_OFM

Data jsou v `../data/2026_4_22_clonky_a_test_mereni`.

## Segmentační labeling

`h5_to_png.py` převede h5 snapshoty z `semgentace_LM5/snapshots` a `semgentace_PC3/snapshots` do PNG do složky `segmetnace_labeling`. Pojmenuje je `img_NN.png` v zamíchaném pořadí (seed 42) a uloží `mapping.json` pro reproducibilitu.

```bash
uv run --with h5py --with numpy --with pillow python h5_to_png.py
```

### Cellpose

Instalace (jednou):

```bash
uv tool install 'cellpose[gui]'
```

Spuštění GUI ve složce s PNG:

```bash
cd ../data/2026_4_22_clonky_a_test_mereni/segmetnace_labeling && uv tool run cellpose
```

Detaily a kontext rozhodnutí: [`docs/segmentation_labeling.md`](docs/segmentation_labeling.md).
