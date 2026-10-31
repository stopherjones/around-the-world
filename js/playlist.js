/*
 * Shared renderer for themed playlist pages.
 *
 * A page opts in by setting data-playlist on <body> to its JSON file, relative
 * to the page, e.g. <body data-playlist="../data/playlists/world-cup-2026.json">.
 * The JSON has the shape: { title, subtitle, spotify_url, theme, tracks: [...] }.
 * Each track has: country, code, track_name, artist_name, spotify_uri, style_note.
 */
(function () {
    const src = document.body.dataset.playlist;
    if (!src) return;

    const listEl = document.getElementById("musicList");
    const searchEl = document.getElementById("searchInput");
    const randomEl = document.getElementById("randomPicker");
    const titleEl = document.getElementById("playlistTitle");
    const subtitleEl = document.getElementById("playlistSubtitle");
    const linkEl = document.getElementById("playlistLink");

    let tracks = [];

    function el(tag, className, text) {
        const node = document.createElement(tag);
        if (className) node.className = className;
        if (text !== undefined && text !== null && text !== "") node.textContent = text;
        return node;
    }

    function makeCard(track) {
        const item = el("div", "music-item");

        const flag = el("div", "flag-thumbnail");
        const img = el("img");
        img.src = `https://flagcdn.com/w160/${track.code}.png`;
        img.alt = `Flag of ${track.country}`;
        img.onerror = () => { img.style.display = "none"; };
        flag.appendChild(img);

        const details = el("div", "music-details");
        details.appendChild(el("div", "country-name", track.country));
        details.appendChild(el("div", "music-artist", track.artist_name));

        const album = el("div", "music-album");
        if (track.spotify_uri) {
            const a = el("a", null, track.track_name || "Listen");
            a.href = track.spotify_uri;
            a.target = "_blank";
            a.rel = "noopener noreferrer";
            album.appendChild(a);
        } else {
            album.textContent = track.track_name || "";
        }
        details.appendChild(album);

        if (track.style_note) details.appendChild(el("div", "music-desc", track.style_note));

        item.append(flag, details);
        return item;
    }

    function matches(track, query) {
        if (!query) return true;
        return [track.country, track.track_name, track.artist_name, track.style_note]
            .some(value => (value || "").toLowerCase().includes(query));
    }

    function render() {
        const query = (searchEl?.value || "").trim().toLowerCase();
        listEl.innerHTML = "";
        const shown = tracks.filter(t => matches(t, query));

        if (shown.length === 0) {
            listEl.appendChild(el("div", "empty-state", "No tracks match that search."));
            return;
        }
        shown.forEach(t => listEl.appendChild(makeCard(t)));
    }

    function pickRandom() {
        const items = listEl.querySelectorAll(".music-item");
        if (!items.length) return;
        const chosen = items[Math.floor(Math.random() * items.length)];
        chosen.scrollIntoView({ behavior: "smooth", block: "center" });
        chosen.classList.add("random-entry-highlight");
        window.setTimeout(() => chosen.classList.remove("random-entry-highlight"), 2000);
    }

    function showError(message) {
        listEl.innerHTML = "";
        listEl.appendChild(el("div", "empty-state", message));
    }

    if (randomEl) randomEl.addEventListener("click", pickRandom);
    if (searchEl) searchEl.addEventListener("input", render);

    fetch(src)
        .then(res => {
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json();
        })
        .then(data => {
            tracks = data.tracks || [];
            if (data.title) {
                document.title = `Around the World - ${data.title}`;
                if (titleEl) titleEl.textContent = data.title;
            }
            if (subtitleEl) subtitleEl.textContent = data.subtitle || "";
            if (linkEl && data.spotify_url) {
                const a = el("a", null, "Spotify playlist here");
                a.href = data.spotify_url;
                a.target = "_blank";
                a.rel = "noopener noreferrer";
                linkEl.appendChild(a);
            } else if (linkEl) {
                linkEl.remove();
            }
            render();
        })
        .catch(err => {
            console.error("Could not load playlist:", err);
            showError("This playlist could not be loaded. Please try again later.");
        });
})();
