# around-the-world
Music and books from around the world

## Data conventions

- **Country names** use the names in `data/countries.json` as the canonical set. Other data files must use the same spelling. Commonwealth Games territories (Anguilla, Bermuda, British Virgin Islands, Cayman Islands, Cook Islands) and Curaçao are allowed outside `data/countries.json`.
- **Dates** in `data/countries.json` music entries and `data/events.json` are `DD-MM` (day first, zero-padded, no year).
- **Spotify links** must start with `https://open.spotify.com/`.
- **Track entries** (`data/highlights.json`, `data/c-games2026.json`) use `country`, `code`, `track_name`, `artist_name`, `spotify_uri` and `style_note`. Don't add a `continent` field to them.
- **Spelling** follows British English (for example "colour", "centre", "defence").

## Checking the data

After any change to the JSON files, run:

```
python3 tools/validate_data.py
```

It exits with an error if a file is malformed, a date is invalid, a link is wrong or a required field is missing. Warnings (for example, a missing style note) don't stop it.

## Repo layout

```
index.html          gallery (home)
books.html          books list
music.html          music list, links to the playlist pages
calendar.html       calendar entries
playlists/          themed playlist pages and playlists/index.html
data/playlists/     one JSON file per playlist (see "Playlists" below)
css/style.css
js/script.js        gallery, books, music and calendar renderer
js/playlist.js      shared renderer for playlist pages
data/               JSON data (countries, events)
images/             calendar and territory images
tools/              validate_data.py
.github/            reminder workflow and check_music.py
WorldCup2026.html, CommonwealthGames2026.html
                    redirects to the playlists/ pages (keep old links working)
favicon.jpg
googleccc77936a16528e9.html   Google verification file (keep in root)
```

## Playlists

Each playlist is a JSON file in `data/playlists/` and a short HTML page in `playlists/`.

The JSON file has this shape:

```json
{
  "title": "Festival of Remembrance",
  "subtitle": "Songs from across Latin America...",
  "spotify_url": "",
  "theme": "remembrance",
  "tracks": [
    {
      "country": "Mexico",
      "code": "mx",
      "track_name": "La Llorona",
      "artist_name": "Chavela Vargas",
      "spotify_uri": "https://open.spotify.com/track/...",
      "style_note": "..."
    }
  ]
}
```

`spotify_url` is optional; leave it empty if there's no playlist link. Tracks appear in the order they're listed.

To add a playlist:

1. Create `data/playlists/<slug>.json` in the shape above.
2. Copy an existing page in `playlists/`, change the `data-playlist` path on `<body>` to the new JSON file, and update the title in the HTML.
3. Add a link to it in `playlists/index.html` and, if it fits, in `music.html`.
4. Run `python3 tools/validate_data.py`.
