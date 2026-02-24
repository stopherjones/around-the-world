import json
import os
from datetime import datetime

data_file = 'countries.json'
today = datetime.now().strftime('%d-%m')

with open(data_file) as f:
    countries = json.load(f)

matches = []
for country in countries:
    music_today = [m for m in country.get('music', []) if m.get('date') == today]
    if music_today:
        matches.append((country, music_today))

if not matches:
    print("No music entries for today.")
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write("has_matches=false\n")
else:
    date_display = datetime.now().strftime('%d %B')
    subject = f"🎵 Music for today ({date_display}): {', '.join(c['name'] for c, _ in matches)}"

    body_parts = [f"<h2>🎵 Your music listening for {date_display}</h2>"]
    
    for country, entries in matches:
        body_parts.append(f"<h3>{country['name']} ({country['continent']})</h3>")
        for entry in entries:
            body_parts.append(f"""
            <div style="margin-bottom:16px; padding:12px; border-left:4px solid #1DB954;">
                <strong>{entry['artist']}</strong> — {entry['album_or_playlist']}<br>
                <em>{entry['description']}</em><br>
                <a href="{entry['url']}">▶ Open in Spotify</a>
            </div>
            """)
        search_url = f"https://www.google.com/search?q=Identify+for+{country['name'].replace(' ', '+')}:+a+traditional+music+genre,+a+modern+mainstream+artist,+and+an+experimental+fusion+act"
        body_parts.append(f'<p><a href="{search_url}">🔍 Explore more music from {country["name"]}</a></p>')
        
        bbc_url = f"https://www.google.com/search?q=BBC+Music+Planet+{country['name'].replace(' ', '+')}"
        guardian_url = f"https://www.google.com/search?q=Guardian+Global+album+of+the+month+{country['name'].replace(' ', '+')}"
        body_parts.append(f'<p><a href="{bbc_url}">🎙️ BBC Music Planet - {country["name"]}</a></p>')
        body_parts.append(f'<p><a href="{guardian_url}">📰 Guardian Global album of the month - {country["name"]}</a></p>')

    body = "\n".join(body_parts)

    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write("has_matches=true\n")
        f.write(f"email_subject={subject}\n")
        f.write(f"email_body<<EOF\n{body}\nEOF\n")
    
    print(f"Found {len(matches)} match(es): {[c['name'] for c, _ in matches]}")