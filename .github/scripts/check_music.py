import json
import os
from datetime import datetime

today = datetime.now().strftime('%d-%m')

# Load countries data
with open('countries.json') as f:
    countries = json.load(f)

# Load events data (safely handle if file doesn't exist yet)
events = []
if os.path.exists('events.json'):
    with open('events.json') as f:
        events = json.load(f)

country_matches = []
for country in countries:
    music_today = [m for m in country.get('music', []) if m.get('date') == today]
    if music_today:
        country_matches.append((country, music_today))

event_matches = [ev for ev in events if ev.get('date') == today]

if not country_matches and not event_matches:
    print("No music entries or events for today.")
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write("has_matches=false\n")
else:
    date_display = datetime.now().strftime('%d %B')
    
    match_names = [c['name'] for c, _ in country_matches] + [ev['event'] for ev in event_matches]
    subject = f"🎵 Music for today ({date_display}): {', '.join(match_names)}"

    body_parts = [f"<h2>🎵 Your music listening for {date_display}</h2>"]
    
    # Render Country Matches (National Days)
    for country, entries in country_matches:
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

        songlines_url = f"https://www.songlines.co.uk/reviews-search?query={country['name'].replace(' ', '+')}"
        beehype_url = f"https://beehy.pe/place/{country['name'].lower().replace(' ', '-')}"
        guardian_url = f"https://www.google.com/search?q=Guardian+Global+album+of+the+month+{country['name'].replace(' ', '+')}"
        body_parts.append(f'<p><a href="{songlines_url}">🎼 Songlines Reviews - {country["name"]}</a></p>')
        body_parts.append(f'<p><a href="{beehype_url}">🫶 Beehype - {country["name"]}</a></p>')
        body_parts.append(f'<p><a href="{guardian_url}">📰 Guardian Global album of the month - {country["name"]}</a></p>')

    # Render Calendar Event Matches
    for eventItem in event_matches:
        body_parts.append(f"<h3>📆 {eventItem['event']}</h3>")
        if eventItem.get('date_note'):
            body_parts.append(f"<p><em>Date: {eventItem['date_note']}</em></p>")
            
        if eventItem.get('music'):
            for m in eventItem['music']:
                artist_text = f"<strong>{m['artist']}</strong> — " if m.get('artist') else ""
                url_tag = f'<a href="{m["url"]}">▶ Open in Spotify</a>' if m.get('url') else m.get('album_or_playlist', '')
                
                body_parts.append(f"""
                <div style="margin-bottom:16px; padding:12px; border-left:4px solid #FF7518;">
                    {artist_text}{m.get('album_or_playlist', '')}<br>
                    <em>{m.get('description', '')}</em><br>
                    {url_tag}
                </div>
                """)
                
        # Embed generic Ecosia search prompt URL for the event
        ecosia_query = f"{eventItem['event']} music playlist OR radio broadcast OR coverage".replace(' ', '+')
        ecosia_url = f"https://www.ecosia.org/search?q={ecosia_query}"
        body_parts.append(f'<p><a href="{ecosia_url}">🔍 Search more coverage for {eventItem["event"]} on Ecosia</a></p>')

    body = "\n".join(body_parts)

    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write("has_matches=true\n")
        f.write(f"email_subject={subject}\n")
        f.write(f"email_body<<EOF\n{body}\nEOF\n")
    
    print(f"Found {len(country_matches)} country match(es) and {len(event_matches)} event match(es).")
