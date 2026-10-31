/*
 * Site navigation, built from one list so every page matches.
 *
 * Each page has:
 *   <div id="site-nav" data-root="">   (data-root is "../" on pages in playlists/)
 *   <body data-nav="music">            (top-level section the page belongs to)
 *   <body data-sub="playlists">        (optional: current item under Music)
 *   <body data-parent="playlists">     (optional: adds a breadcrumb back to that item)
 *
 * Calendar and Playlists sit under Music, so their pages use data-nav="music".
 * Music's sub-items sit beside Music when they fit. When they don't, they
 * appear in a second row underneath.
 */
(function () {
    const host = document.getElementById("site-nav");
    if (!host) return;

    const root = host.dataset.root || "";
    const body = document.body;
    const inMusic = body.dataset.nav === "music";

    const sections = [
        { key: "gallery", label: "Gallery", href: "index.html" },
        { key: "books",   label: "Books",   href: "books.html" },
        { key: "music",   label: "Music",   href: "music.html" }
    ];

    // Music's own page is "Music", so only the other pages sit beneath it
    const musicSubs = [
        { key: "playlists", label: "Playlists", href: "playlists/index.html" },
        { key: "calendar",  label: "Calendar",  href: "calendar.html" }
    ];

    function link(item, className, isCurrent) {
        const a = document.createElement("a");
        a.className = className;
        a.href = root + item.href;
        a.textContent = item.label;
        if (isCurrent) a.setAttribute("aria-current", "page");
        return a;
    }

    function inlineMusicGroup() {
        const group = document.createElement("span");
        group.className = "pill-group";
        group.appendChild(link(sections[2], "pill", true));
        musicSubs.forEach(sub =>
            group.appendChild(link(sub, "pill sub", body.dataset.sub === sub.key)));
        return group;
    }

    function subRow() {
        const row = document.createElement("div");
        row.className = "site-subrow";
        row.setAttribute("aria-label", "Music sections");
        musicSubs.forEach(sub =>
            row.appendChild(link(sub, "pill", body.dataset.sub === sub.key)));
        return row;
    }

    function build(separateSubRow) {
        host.querySelectorAll(".site-nav, .site-subrow, .breadcrumb").forEach(node => node.remove());

        const row = document.createElement("nav");
        row.className = "site-nav";
        row.setAttribute("aria-label", "Site");

        sections.forEach(section => {
            if (section.key === "music" && inMusic) {
                row.appendChild(separateSubRow
                    ? link(section, "pill", true)
                    : inlineMusicGroup());
            } else {
                row.appendChild(link(section, "pill", body.dataset.nav === section.key));
            }
        });
        host.appendChild(row);
        if (inMusic && separateSubRow) host.appendChild(subRow());

        // Breadcrumb for pages nested under a sub-item (e.g. a playlist page)
        const parentKey = body.dataset.parent;
        if (parentKey) {
            const parent = musicSubs.find(i => i.key === parentKey) || sections.find(i => i.key === parentKey);
            const heading = document.querySelector("h1");
            if (parent) {
                const crumbs = document.createElement("nav");
                crumbs.className = "breadcrumb";
                crumbs.setAttribute("aria-label", "Breadcrumb");
                const back = document.createElement("a");
                back.href = root + parent.href;
                back.textContent = parent.label;
                crumbs.appendChild(back);
                if (heading) {
                    crumbs.appendChild(document.createTextNode(" › "));
                    const here = document.createElement("span");
                    here.textContent = heading.textContent;
                    crumbs.appendChild(here);
                }
                host.appendChild(crumbs);
            }
        }
        return row;
    }

    function layout() {
        let row = build(false);
        if (inMusic && row.scrollWidth > row.clientWidth + 1) {
            row = build(true);
        }
        document.documentElement.style.setProperty("--nav-h", host.offsetHeight + "px");
    }

    layout();
    let lastWidth = host.clientWidth;
    const relayout = () => {
        if (host.clientWidth !== lastWidth) {
            lastWidth = host.clientWidth;
            layout();
        }
    };
    if ("ResizeObserver" in window) {
        new ResizeObserver(relayout).observe(document.documentElement);
    } else {
        window.addEventListener("resize", relayout);
    }
})();
