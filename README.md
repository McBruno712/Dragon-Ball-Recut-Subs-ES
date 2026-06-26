# dbsubs-lat

Translates the English ASS subtitles embedded in the fanmade **Dragon Ball Recut v2** `.mkv` collection to Latin-American Spanish.

Outputs a separate `*.ES.ass` next to each source video. The `.mkv` files are never modified.

## Usage

```bash
cd ~/repos/dbsubs-lat
source venv/bin/activate
python -m dbsubs_lat.cli \
  --videos-dir "/home/mcbruno712/Videos/Películas/Dragon Ball Recut (Complete) v2" \
  --pilot E01
```

## Layout

- `src/dbsubs_lat/` — source code
- `data/glosario_latino.json` — proper-noun glossary
- `tests/` — pytest suite
- `logs/` — per-episode processing reports (gitignored)
