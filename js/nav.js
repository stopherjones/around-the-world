/*
 * Site navigation, built from one list so every page matches.
 *
 * Each page has:
 *   <div id="site-nav" data-root="">   (data-root is "../" on pages in playlists/)
 *   <body data-nav="books">            (which top-level section this page belongs to)
 *   <body data-parent="playlists">     (optional: shows a breadcrumb back to that section)
 */
(function () {
    const host = document.getElementById("site-nav");
    if (!host) return;

    const root = host.dataset.root || "";
    const current = document.body.dataset.nav || "";
    const parent = document.body.dataset.parent || "";

    const sections = [
        { key: "gallery",   label: "Gallery",   href: "index.html" },
        { key: "books",     label: "Books",     href: "books.html" },
        { key: "music",     label: "Music",     href: "music.html" },
        { key: "playlists", label: "Playlists", href: "playlists/index.html" },
        { key: "calendar",  label: "Calendar",  href: "calendar.html" }
    ];

    const nav = document.createElement("nav");
    nav.className = "site-nav";
    nav.setAttribute("aria-label", "Site");

    sections.forEach(section => {
        const a = document.createElement("a");
        a.className = "top-link";
        a.href = root + section.href;
        a.textContent = section.label;
        if (section.key === current) a.setAttribute("aria-current", "page");
        nav.appendChild(a);
    });
    host.appendChild(nav);

    if (parent) {
        const section = sections.find(s => s.key === parent);
        const heading = document.querySelector("h1");
        if (section) {
            const crumbs = document.createElement("nav");
            crumbs.className = "breadcrumb";
            crumbs.setAttribute("aria-label", "Breadcrumb");

            const back = document.createElement("a");
            back.href = root + section.href;
            back.textContent = section.label;
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
})();
