# SDB food library

One checked cut-out per dish, for every Shuddh Desi Bites reel, carousel and post. Used by the `sdb-food-images` skill.

- `meals/tray/`: real meals in clean delivery trays (food unchanged; trays are AI-made, so posts need the AI label).
- `drinks/`, `snacks/`: dishes cut whole from the owner's photos, shape-fitted to the container rim (never colour-keyed).
- `manifest.json`: name, file, kind, cut method, view, date checked, menu status.
- `contact-sheet.jpg`: every image on light and dark backgrounds, for a quick edge check.
- `tools/food_fit.py`: checks every placed dish stays whole in the 1080x1920 frame at the scene's largest zoom (24 px margin).
- `tools/cut_plate.py`, `tray_on_table.py`, `tray_persp.py`: cut a round plate, set a tray on a top-down table, or lay one on an eye-level table in perspective.

Add a dish: cut it from the owner's real photo, check it on the contact sheet, add it to the manifest, and commit here.
