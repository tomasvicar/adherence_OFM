# adherence_OFM

Data jsou v `../data/2026_4_22_clonky_a_test_mereni`.

## Segmentační labeling

`h5_to_png.py` převede h5 snapshoty z `semgentace_LM5/snapshots` a `semgentace_PC3/snapshots` do PNG do složky `segmetnace_labeling`. Pojmenuje je `img_NN.png` v zamíchaném pořadí (seed 42) a uloží `mapping.json` pro reproducibilitu.

```bash
uv run --with h5py --with numpy --with pillow python h5_to_png.py
```

`h5_to_png_small.py` totéž, ale udělá z každého obrázku 3 náhodné čtvercové výřezy 360×360 px, všechny dohromady promíchá (seed 43) a uloží do `segmetnace_labeling_small`. Na menších výřezech se značí přesněji.

```bash
uv run --with h5py --with numpy --with pillow python h5_to_png_small.py
```

### Cellpose

Instalace (jednou) — **GPU verze, doporučená** (PyTorch s CUDA 12.8):

```bash
uv tool install --link-mode=copy --index https://download.pytorch.org/whl/cu128 --index-strategy unsafe-best-match 'cellpose[gui]'
```

Pokud GPU nemáš, stačí CPU verze:

```bash
uv tool install --link-mode=copy 'cellpose[gui]'
```

Po instalaci je `cellpose` přímo na PATH. Spuštění GUI ve složce s PNG (dva řádky, funguje v PowerShellu i bashi):

```
cd ../data/2026_4_22_clonky_a_test_mereni/segmetnace_labeling
cellpose
```

Ověření, že cellpose běží na GPU:

```bash
cellpose --version
```

Mělo by vypsat `torch version: 2.11.0+cu128` (GPU) místo `+cpu`. V GUI pak zaškrtni *use GPU*.

Pozn.: `--link-mode=copy` obchází chybu *"failed to hardlink"* / *"cloud operation cannot be performed on a file with incompatible hardlinks"*, která se objeví, když uv cache (`%LOCALAPPDATA%\uv\cache`) a cíl jsou na různých svazcích / OneDrive. Alternativně lze nastavit jednou:

```powershell
[Environment]::SetEnvironmentVariable("UV_LINK_MODE", "copy", "User")
```

(po nastavení znovu otevři terminál, pak už `--link-mode=copy` přidávat nemusíš).

Přepnutí mezi CPU/GPU buildem: `uv tool uninstall cellpose` a znovu spustit příslušný `uv tool install` výše.

Detaily a kontext rozhodnutí: [`docs/segmentation_labeling.md`](docs/segmentation_labeling.md).
