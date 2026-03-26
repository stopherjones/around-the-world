# Around the World in Books and Music

A personal tracking and showcase website for music and books from various countries and territories.

## Architecture

- **Type:** Pure static site — HTML, CSS, and vanilla JavaScript (no build system)
- **Data:** JSON files (`countries.json`, `highlights.json`)
- **External APIs:** FlagCDN for flag images, Spotify links for music

## Project Structure

```
index.html            # Main gallery view
books.html            # Books list view
music.html            # Music list view
music-highlights.html # Music highlights view
script.js             # Core logic (fetch JSON, render gallery, popups, filtering)
style.css             # Styles (responsive, popup overlay)
countries.json        # Country/book/music data
highlights.json       # Music highlights data
images/               # Local flag image overrides (England, Scotland, Wales, Scilly)
```

## Running

Served via Python's built-in HTTP server:

```
python3 -m http.server 5000 --bind 0.0.0.0
```

Workflow: **Start application** on port 5000.

## Deployment

Configured as a **static** deployment with `publicDir: "."`.
