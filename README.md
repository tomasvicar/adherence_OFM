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
uv tool install --link-mode=copy 'cellpose[gui]'
```

Spuštění GUI ve složce s PNG (dva řádky, funguje v PowerShellu i bashi):

```
cd ../data/2026_4_22_clonky_a_test_mereni/segmetnace_labeling
uv tool run --link-mode=copy cellpose
```

Pozn.: `--link-mode=copy` obchází chybu *"failed to hardlink"* / *"cloud operation cannot be performed on a file with incompatible hardlinks"*, která se objeví, když uv cache (`%LOCALAPPDATA%\uv\cache`) a cíl jsou na různých svazcích / OneDrive. Alternativně lze nastavit jednou:

```powershell
[Environment]::SetEnvironmentVariable("UV_LINK_MODE", "copy", "User")
```

(po nastavení znovu otevři terminál, pak už `--link-mode=copy` přidávat nemusíš).

Detaily a kontext rozhodnutí: [`docs/segmentation_labeling.md`](docs/segmentation_labeling.md).
