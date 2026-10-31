#!/usr/bin/env python3
"""Validate the site's JSON data files.

Run from the repo root:  python3 tools/validate_data.py
Exits with status 1 if any errors are found. Warnings do not fail the run.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors, warnings = [], []

# Country names that are allowed outside data/countries.json (e.g. Commonwealth
# Games territories, and Curaçao, which is not a separate entry there).
EXTRA_NAMES = {
    "Curaçao", "Anguilla", "Bermuda", "British Virgin Islands",
    "Cayman Islands", "Cook Islands",
}
VALID_CONTINENTS = {"Africa", "Asia", "Europe", "North America", "South America", "Oceania"}
DATE_RE = re.compile(r"^(\d{2})-(\d{2})$")  # DD-MM


def load(name):
    with open(ROOT / name, encoding="utf-8") as f:
        return json.load(f)


def check_date(where, value):
    m = DATE_RE.match(value or "")
    if not m:
        errors.append(f"{where}: date '{value}' is not DD-MM")
        return
    day, month = int(m.group(1)), int(m.group(2))
    if not (1 <= month <= 12 and 1 <= day <= 31):
        errors.append(f"{where}: date '{value}' is not a real day and month")


def check_spotify(where, uri):
    if not (uri or "").startswith("https://open.spotify.com/"):
        errors.append(f"{where}: spotify link '{uri}' should start with https://open.spotify.com/")


countries = load("data/countries.json")
names = [c["name"] for c in countries]
codes = [c["code"] for c in countries]
for dup in {n for n in names if names.count(n) > 1}:
    errors.append(f"data/countries.json: duplicate name '{dup}'")
for dup in {c for c in codes if codes.count(c) > 1}:
    errors.append(f"data/countries.json: duplicate code '{dup}'")

for c in countries:
    where = f"data/countries.json [{c.get('name')}]"
    for key in ("name", "code", "type", "continent", "read", "books", "music"):
        if key not in c:
            errors.append(f"{where}: missing '{key}'")
    if c.get("continent") not in VALID_CONTINENTS:
        errors.append(f"{where}: continent '{c.get('continent')}' is not one of {sorted(VALID_CONTINENTS)}")
    for b in c.get("books", []):
        if not b.get("title") or not b.get("author"):
            errors.append(f"{where}: book missing title or author")
    for m in c.get("music", []):
        check_date(where, m.get("date")) if "date" in m else None
        check_spotify(where, m.get("url"))
        for key in ("artist", "album_or_playlist", "url"):
            if key not in m:
                errors.append(f"{where}: music entry missing '{key}'")

known = set(names) | EXTRA_NAMES
import glob
for path in sorted(glob.glob(str(ROOT / "data" / "playlists" / "*.json"))):
    fname = "data/playlists/" + Path(path).name
    playlist = json.load(open(path, encoding="utf-8"))
    for key in ("title", "subtitle", "tracks"):
        if key not in playlist:
            errors.append(f"{fname}: missing '{key}'")
    for i, e in enumerate(playlist.get("tracks", [])):
        where = f"{fname} #{i + 1} [{e.get('country')}]"
        if e.get("country") not in known:
            warnings.append(f"{where}: country name not in data/countries.json (check spelling)")
        if "track_name" not in e:
            errors.append(f"{where}: missing 'track_name'")
        if "continent" in e:
            errors.append(f"{where}: 'continent' should not be on a track entry")
        check_spotify(where, e.get("spotify_uri"))
        if not e.get("style_note"):
            warnings.append(f"{where}: no style_note")

events = load("data/events.json")
for i, ev in enumerate(events):
    where = f"data/events.json #{i + 1} [{ev.get('event', '?')}]"
    check_date(where, ev.get("date"))

if errors:
    print("ERRORS:")
    for e in errors:
        print("  -", e)
if warnings:
    print("WARNINGS:")
    for w in warnings:
        print("  -", w)
if not errors and not warnings:
    print("All data files look good.")
print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
