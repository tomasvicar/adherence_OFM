# Segmentační labeling — postup

Záznam přípravy dat pro ruční tvorbu segmentačních masek v Cellpose.

## Vstup

H5 snapshoty pořízené softwarem [open-flexure-custom-sw](https://github.com/tomasvicar/open-flexure-custom-sw):

- `data/2026_4_22_clonky_a_test_mereni/semgentace_LM5/snapshots/*.h5` (29 souborů)
- `data/2026_4_22_clonky_a_test_mereni/semgentace_PC3/snapshots/*.h5` (32 souborů)

Každý h5 obsahuje `images/data` tvaru `(1, H, W, 3) uint8` a atributy včetně `rotation`, `mirror`, `experiment`, `note` atd.

## Výstup

Složka `data/2026_4_22_clonky_a_test_mereni/segmetnace_labeling/`:

- 61 PNG `img_00.png` … `img_60.png` v náhodně promíchaném pořadí (LM5 a PC3 promíchané dohromady)
- `mapping.json` — mapování nového názvu zpět na zdrojovou složku a originální `.h5` cestu, plus `seed` a per-soubor záznam atributů `rotation`/`mirror`

Skript: [`../h5_to_png.py`](../h5_to_png.py). Seed pro shuffle je `42` (`random.Random(SEED)`), takže běh je deterministický a šlo by ho zopakovat / ověřit.

## Rozhodnutí: žádná rotace/zrcadlení při exportu

Atributy `rotation` a `mirror` v h5 souborech jsou **záznam toho, co bylo aplikováno při ukládání snapshotu**, ne instrukce k aplikaci při čtení.

Důkazy z [open-flexure-custom-sw](https://github.com/tomasvicar/open-flexure-custom-sw):

- `custom_things/recorder.py` — `snapshot()` volá `arr = _apply_transform(arr, rotation, mirror)` **před** zápisem do h5. Pixely v `images/data` jsou tedy již v zobrazovací orientaci.
- `custom_things/static/data_viewer/index.html` — komentář u `currentIsSnapshot`:

  ```js
  let currentIsSnapshot = false;  /* true when viewing an H5 snapshot (transform already baked in) */
  ```

  a o pár řádků níže:

  ```js
  /* For recordings, apply camera transform; for snapshots it's already baked in */
  if (!currentIsSnapshot) { ... }
  ```

  Tedy viewer pro snapshoty žádnou transformaci neaplikuje.

Konvence (pro pozdější referenci, když by se přepisovaly *recordings*, ne snapshots):

- `mirror` se aplikuje **před** rotací (aby odpovídalo CSS `transform: rotate(X) scaleX(-1)`, které vyhodnocuje zprava doleva).
- `rotation` je ve stupních **CW**: `90 → np.rot90(k=3)`, `180 → k=2`, `270 → k=1`.

## Cellpose

Verze: `cellpose 4.1.1`, instalovaný přes `uv tool install 'cellpose[gui]'`. Běží na CPU (PyTorch wheel pro Windows nepřišel s CUDA buildem) — auto-segmentace je pomalejší, ale ruční labeling funguje normálně.

Spuštění:

```bash
cd ../data/2026_4_22_clonky_a_test_mereni/segmetnace_labeling
uv tool run cellpose
```

V GUI: *File → Load image* a otevřít konkrétní `img_NN.png`. Cellpose ukládá masky a outliny vedle obrázku.
