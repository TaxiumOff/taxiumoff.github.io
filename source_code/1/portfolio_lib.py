#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fonctions partagées pour lire, générer et modifier les projets du portfolio.

Ce module ne dépend que de la bibliothèque standard Python. Il sert à la fois
aux scripts console et à l'application graphique project_manager.py.
"""

import re
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
SOURCE_DIR = ROOT / "source_code"

MARKERS = {
    "petit": ("<!-- BEGIN SMALL PROJECTS -->", "<!-- END SMALL PROJECTS -->"),
    "gros": ("<!-- BEGIN BIG PROJECTS -->", "<!-- END BIG PROJECTS -->"),
}

SIZES = {
    "1": {"value": "petit", "label": "Projet personnel", "section": "Projets personnels"},
    "2": {"value": "gros", "label": "Projet majeur", "section": "Projets majeurs"},
}
SIZE_VALUES = {item["value"]: item for item in SIZES.values()}
SIZE_ORDER = ["petit", "gros"]

CATEGORIES = {
    "1": {"value": "jeux-video", "label": "Jeux vidéo", "thumb": "thumb--one"},
    "2": {"value": "cybersecurite", "label": "Cybersécurité", "thumb": "thumb--two"},
}
CATEGORY_VALUES = {item["value"]: item for item in CATEGORIES.values()}
CATEGORY_LABELS = {
    item["value"]: item["label"] for item in CATEGORIES.values()
}

LANGUAGES = {
    "1": {
        "value": "python",
        "label": "Python",
        "badge": "lang-python",
        "icon": "M11.858 0c-.978.005-1.913.088-2.736.234C6.7.662 6.26 1.558 6.26 3.21v2.182h5.725v.727H4.111c-1.664 0-3.121 1-3.577 2.903-.526 2.181-.549 3.542 0 5.82.407 1.694 1.379 2.902 3.043 2.902h1.969v-2.616c0-1.89 1.635-3.557 3.576-3.557h5.72c1.591 0 2.862-1.31 2.862-2.91v-5.45c0-1.553-1.309-2.718-2.863-2.977A18 18 0 0 0 11.858 0M8.762 1.755c.591 0 1.074.491 1.074 1.095 0 .601-.483 1.087-1.074 1.087A1.08 1.08 0 0 1 7.688 2.85c0-.604.48-1.095 1.074-1.095m9.656 4.364v2.543c0 1.971-1.671 3.63-3.577 3.63H9.122c-1.566 0-2.862 1.34-2.862 2.91v5.452c0 1.551 1.349 2.464 2.862 2.91 1.813.532 3.55.628 5.72 0 1.44-.418 2.862-1.258 2.862-2.91V18.47h-5.719v-.727h8.582c1.664 0 2.284-1.16 2.862-2.903.598-1.793.573-3.518 0-5.819-.41-1.656-1.196-2.903-2.862-2.903zm-3.216 13.807a1.08 1.08 0 0 1 1.074 1.088c0 .604-.48 1.094-1.074 1.094-.592 0-1.075-.49-1.075-1.094 0-.601.483-1.088 1.075-1.088",
    },
    "2": {
        "value": "cpp",
        "label": "C++",
        "badge": "lang-cpp",
        "icon": "M22.394 6c-.167-.29-.398-.543-.652-.69L12.926.22c-.509-.294-1.34-.294-1.848 0L2.26 5.31c-.508.293-.923 1.013-.923 1.6v10.18c0 .294.104.62.271.91.167.29.398.543.652.69l8.816 5.09c.508.293 1.34.293 1.848 0l8.816-5.09c.254-.147.485-.4.652-.69.167-.29.27-.616.27-.91V6.91c.003-.294-.1-.62-.268-.91zM12 19.11c-3.92 0-7.109-3.19-7.109-7.11 0-3.92 3.19-7.11 7.11-7.11a7.133 7.133 0 016.156 3.553l-3.076 1.78a3.567 3.567 0 00-3.08-1.78A3.56 3.56 0 008.444 12 3.56 3.56 0 0012 15.555a3.57 3.57 0 003.08-1.778l3.078 1.78A7.135 7.135 0 0112 19.11zm7.11-6.715h-.79v.79h-.79v-.79h-.79v-.79h.79v-.79h.79v.79h.79zm2.962 0h-.79v.79h-.79v-.79h-.79v-.79h.79v-.79h.79v.79h.79z",
    },
}
LANGUAGE_VALUES = {item["value"]: item for item in LANGUAGES.values()}
LANGUAGE_LABELS = {
    item["value"]: item["label"] for item in LANGUAGES.values()
}

THUMBS = {
    "thumb--one": {"number": "1", "label": "Violet"},
    "thumb--two": {"number": "2", "label": "Vert"},
    "thumb--three": {"number": "3", "label": "Orange"},
}

DEFAULT_THUMBS = {
    "jeux-video": "thumb--one",
    "cybersecurite": "thumb--two",
}


class PortfolioError(Exception):
    """Erreur attendue liée à la structure de index.html."""


def clean_text(fragment: str) -> str:
    """Retire les balises d'un fragment HTML et décode les entités."""
    text = re.sub(r"<[^>]+>", " ", fragment)
    return " ".join(unescape(text).split())


def read_attribute(block: str, name: str) -> str:
    """Lit un attribut sur la balise <article> du projet."""
    match = re.search(rf'{name}="([^"]*)"', block)
    return match.group(1) if match else ""


def find_section(block: str, pattern: str) -> str:
    """Renvoie le contenu HTML de la première section correspondante."""
    match = re.search(pattern, block, re.S)
    return match.group(1) if match else ""


def safe_href(href: str) -> str:
    """Refuse les URL non http(s) pour éviter javascript: ou data:."""
    href = href.strip()
    if not href:
        return ""
    if not re.match(r"^https?://", href, re.I):
        raise PortfolioError(
            f"Lien invalide : « {href} ». Utilise une adresse commençant par http:// ou https://."
        )
    return href


def make_link(href: str, label: str, aria: str) -> str:
    """Construit un lien externe sécurisé, ou une chaîne vide si pas d'URL."""
    href = safe_href(href)
    if not href:
        return ""
    safe_href_value = escape(href, quote=True)
    safe_aria = escape(aria, quote=True)
    return (
        f'<a href="{safe_href_value}" target="_blank" rel="noopener noreferrer" '
        f'aria-label="{safe_aria} (nouvel onglet)">'
        f'{label} <span aria-hidden="true">→</span></a>'
    )


def parse_tags(tags: str) -> str:
    """Transforme une liste séparée par des virgules en <li> échappés."""
    items = "".join(
        f"<li>{escape(tag.strip())}</li>" for tag in tags.split(",") if tag.strip()
    )
    return items


def normalize_asset_path(value: str) -> str:
    """Accepte uniquement un chemin relatif sûr, avec des slashs URL."""
    value = (value or "").strip().replace("\\", "/")
    if not value:
        return ""
    parts = value.split("/")
    if value.startswith("/") or ".." in parts or ":" in parts[0]:
        raise PortfolioError(f"Chemin de fichier invalide : {value}")
    return value


def normalize_project(data: dict) -> dict:
    """Vérifie et normalise les valeurs avant génération du HTML."""
    size = data.get("size", "petit")
    if size not in SIZE_VALUES:
        raise PortfolioError(f"Type de projet inconnu : {size}")

    category = data.get("category", "jeux-video")
    if category not in CATEGORY_VALUES:
        raise PortfolioError(f"Catégorie inconnue : {category}")

    language = data.get("language", "python")
    if language not in LANGUAGE_VALUES:
        raise PortfolioError(f"Langage inconnu : {language}")

    thumb = data.get("thumb") or DEFAULT_THUMBS[category]
    if thumb not in THUMBS:
        raise PortfolioError(f"Style de vignette inconnu : {thumb}")

    name = data.get("name", "").strip()
    if not name:
        raise PortfolioError("Le nom du projet est obligatoire.")

    safe_links = {
        key: safe_href(data.get(key, "")) for key in ("demo", "source")
    }

    return {
        "size": size,
        "name": name,
        "date": data.get("date", "").strip(),
        "category": category,
        "language": language,
        "description": data.get("description", "").strip(),
        "tags": data.get("tags", "").strip(),
        "demo": safe_links["demo"],
        "source": safe_links["source"],
        "thumb": thumb,
        "code_file": normalize_asset_path(data.get("code_file", "")),
        "report_file": normalize_asset_path(data.get("report_file", "")),
        "report_text": data.get("report_text", "").strip(),
    }


def build_code_viewer(project: dict) -> str:
    """Prépare le lecteur de code et le rapport, en lecture seule."""
    if not project["code_file"] and not project["report_file"] and not project["report_text"]:
        return ""

    parts = [
        '<details class="code-viewer">',
        '<summary class="code-viewer__toggle">'
        '<span class="code-viewer__label">Voir le code et le rapport</span>'
        '<span class="code-viewer__hint">Lecture seule</span>'
        '<span class="code-viewer__chevron" aria-hidden="true">⌄</span>'
        "</summary>",
    ]

    if project["code_file"]:
        code_path = escape(project["code_file"], quote=True)
        file_name = escape(project["code_file"].split("/")[-1])
        parts.append(
            '<div class="code-editor">'
            '<div class="code-editor__bar">'
            '<span class="code-editor__dots" aria-hidden="true"><i></i><i></i><i></i></span>'
            f'<span class="code-editor__file">{file_name}</span>'
            '<span class="code-editor__mode">Lecture seule</span>'
            "</div>"
            '<div class="code-editor__scroll">'
            '<pre class="code-editor__gutter" aria-hidden="true"></pre>'
            f'<pre class="code-editor__body"><code data-code-src="{code_path}">Chargement du code…</code></pre>'
            "</div>"
            "</div>"
        )

    if project["report_file"]:
        report_path = escape(project["report_file"], quote=True)
        parts.append(
            '<div class="code-report">'
            '<h4>À propos du code</h4>'
            f'<div class="code-report__body" data-report-src="{report_path}">Chargement du rapport…</div>'
            "</div>"
        )
    elif project["report_text"]:
        parts.append(
            '<div class="code-report">'
            "<h4>À propos du code</h4>"
            f'<div class="code-report__body">{escape(project["report_text"])}</div>'
            "</div>"
        )

    parts.append("</details>")
    return "\n".join(parts)


def build_card(data: dict) -> str:
    """Génère une vitrine pour un projet majeur, une carte compacte sinon."""
    project = normalize_project(data)
    size = SIZE_VALUES[project["size"]]
    category = CATEGORY_VALUES[project["category"]]
    language = LANGUAGE_VALUES[project["language"]]

    tag_items = parse_tags(project["tags"])
    if not tag_items:
        tag_items = f"<li>{language['label']}</li>"

    links = "".join(
        link
        for link in (
            make_link(project["demo"], "Voir le projet", f"Voir {project['name']}"),
            make_link(
                project["source"], "Code source", f"Code source de {project['name']}"
            ),
        )
        if link
    )
    if not links:
        links = '<span class="project-card__soon">Lien bientôt disponible</span>'

    lang_icon = (
        '<svg class="lang-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        f'<path d="{language["icon"]}"/></svg>'
    )
    lang_badge = (
        f'<span class="project-card__lang {language["badge"]}">'
        f'{lang_icon}{language["label"]}</span>'
    )

    code_attrs = ""
    if project["code_file"]:
        code_attrs += f' data-code-file="{escape(project["code_file"], quote=True)}"'
    if project["report_file"]:
        code_attrs += f' data-report-file="{escape(project["report_file"], quote=True)}"'

    meta = escape(project["date"]) if project["date"] else size["label"]
    if project["date"]:
        meta = f"{meta} · {size['label']}"

    viewer = build_code_viewer(project)

    if project["size"] == "gros":
        return f'''<article class="project-showcase reveal" data-category="{project["category"]}" data-language="{project["language"]}"{code_attrs}>
  <div class="project-showcase__visual {project["thumb"]}">
    <span class="project-card__badge">{category["label"]}</span>
    {lang_badge}
    <span class="project-showcase__index" aria-hidden="true"></span>
    <span class="project-showcase__title">{escape(project["name"])}</span>
    <span class="project-card__arrow" aria-hidden="true">↗</span>
  </div>
  <div class="project-showcase__content">
    <p class="project-card__meta">{meta}</p>
    <h3>{escape(project["name"])}</h3>
    <p>{escape(project["description"])}</p>
    <ul class="tags">{tag_items}</ul>
    <div class="project-card__footer">
      {links}
    </div>
    {viewer}
  </div>
</article>'''

    return f'''<article class="project-card project-card--small reveal" data-category="{project["category"]}" data-language="{project["language"]}"{code_attrs}>
  <div class="project-card__thumb {project["thumb"]}">
    <span class="project-card__badge">{category["label"]}</span>
    {lang_badge}
    <span class="project-card__arrow" aria-hidden="true">↗</span>
  </div>
  <div class="project-card__body">
    <p class="project-card__meta">{meta}</p>
    <h3>{escape(project["name"])}</h3>
    <p>{escape(project["description"])}</p>
    <ul class="tags">{tag_items}</ul>
  </div>
  <div class="project-card__footer">
    {links}
  </div>
  {viewer}
</article>'''


def get_markers(size_value: str, lines: list) -> tuple[int, int]:
    """Renvoie les indices des marqueurs BEGIN/END pour le type demandé."""
    if size_value not in MARKERS:
        raise PortfolioError(f"Type de projet inconnu : {size_value}")
    begin, end = MARKERS[size_value]
    starts = [i for i, line in enumerate(lines) if line.strip() == begin]
    ends = [i for i, line in enumerate(lines) if line.strip() == end]

    if not starts or not ends or ends[0] <= starts[0]:
        raise PortfolioError(
            f"Marqueurs introuvables ou mal placés dans {INDEX.name}."
        )
    return starts[0], ends[0]


def parse_projects(lines: list, start: int, end: int, size_value: str) -> list[dict]:
    """Liste les blocs <article> présents entre les deux marqueurs."""
    projects = []
    index = start + 1

    while index < end:
        line = lines[index]
        if "<article" not in line.lower() or line.lstrip().startswith("<!--"):
            index += 1
            continue

        block_start = index
        depth = 0
        block_lines = []

        while index < end:
            current = lines[index]
            block_lines.append(current)
            lowered = current.lower()
            depth += lowered.count("<article") - lowered.count("</article>")
            index += 1
            if depth <= 0:
                break

        if depth > 0:
            raise PortfolioError("Bloc de projet non fermé : vérifie index.html.")

        block = "\n".join(block_lines)
        projects.append(
            extract_project(block, size_value, block_start, index)
        )

    return projects


def extract_description(block: str, name: str, date: str, size_value: str) -> str:
    """Isole la description du projet sans inclure métadonnées, titre et liens."""
    if "project-showcase__content" in block:
        content = find_section(
            block, r'<div class="project-showcase__content"[^>]*>(.*?)</div>'
        )
    else:
        content = find_section(block, r'<div class="project-card__body"[^>]*>(.*?)</div>')

    size_label = SIZE_VALUES.get(size_value, {}).get("label", "")
    paragraphs = re.findall(r"<p\b[^>]*>(.*?)</p>", content, re.S)
    description = ""
    for paragraph in paragraphs:
        text = clean_text(paragraph)
        if not text or text == size_label or text == f"{date} · {size_label}":
            continue
        description = text
        break

    if not description and content:
        description = clean_text(re.sub(r"<ul\b.*?</ul>", "", content, flags=re.S))
        description = description.removeprefix(name).strip(" ·").strip()

    return description


def extract_project(block: str, size_value: str, start: int, end: int) -> dict:
    """Extrait les champs modifiables d'un bloc <article>."""
    title = find_section(
        block,
        r'<span class="project-showcase__title"[^>]*>(.*?)</span>',
    )
    name = clean_text(title)
    if not name:
        name = clean_text(find_section(block, r"<h3[^>]*>(.*?)</h3>"))
    if not name:
        name = "Sans nom"

    meta_text = clean_text(
        find_section(block, r'<p class="project-card__meta"[^>]*>(.*?)</p>')
    )
    date = meta_text.split("·")[0].strip() if "·" in meta_text else meta_text

    description = extract_description(block, name, date, size_value)

    tag_block = find_section(block, r"<ul class=\"tags\">(.*?)</ul>")
    tags = ", ".join(
        clean_text(item) for item in re.findall(r"<li[^>]*>(.*?)</li>", tag_block, re.S)
    )

    links = {}
    for key, pattern in (
        ("demo", r'<a\b[^>]*href="([^"]+)"[^>]*>\s*Voir le projet'),
        ("source", r'<a\b[^>]*href="([^"]+)"[^>]*>\s*Code source'),
    ):
        match = re.search(pattern, block, re.S)
        links[key] = unescape(match.group(1)) if match else ""

    thumb_match = re.search(
        r'class="(?:project-showcase__visual|project-card__thumb)\s+(thumb--[a-z]+)"',
        block,
    )
    thumb = thumb_match.group(1) if thumb_match else DEFAULT_THUMBS.get(
        read_attribute(block, "data-category"), "thumb--one"
    )

    report_text = clean_text(
        find_section(block, r'<div class="code-report__body"[^>]*>(.*?)</div>')
    )
    if report_text.startswith("Chargement du rapport"):
        report_text = ""

    return {
        "start": start,
        "end": end,
        "size": size_value,
        "name": name,
        "date": date,
        "category": read_attribute(block, "data-category") or "jeux-video",
        "language": read_attribute(block, "data-language") or "python",
        "description": description,
        "tags": tags,
        "demo": links["demo"],
        "source": links["source"],
        "thumb": thumb,
        "code_file": read_attribute(block, "data-code-file"),
        "report_file": read_attribute(block, "data-report-file"),
        "report_text": report_text,
        "block": block,
    }


def read_index() -> tuple[str, list[str]]:
    """Lit index.html et renvoie son contenu avec une liste de lignes."""
    if not INDEX.exists():
        raise PortfolioError(f"Introuvable : {INDEX}")
    content = INDEX.read_text(encoding="utf-8")
    return content, content.splitlines()


def load_projects() -> dict[str, list[dict]]:
    """Détecte tous les projets présents dans les deux grilles."""
    _, lines = read_index()
    projects = {}
    for size_value in SIZE_ORDER:
        start, end = get_markers(size_value, lines)
        projects[size_value] = parse_projects(lines, start, end, size_value)
    return projects


def write_index(lines: list[str], trailing_newline: bool = True) -> None:
    """Réécrit index.html en conservant la fin de ligne finale."""
    INDEX.write_text(
        "\n".join(lines) + ("\n" if trailing_newline else ""), encoding="utf-8"
    )


def insert_card(data: dict) -> dict:
    """Ajoute une carte juste avant le marqueur END correspondant."""
    content, lines = read_index()
    project = normalize_project(data)
    start, end = get_markers(project["size"], lines)

    marker_line = lines[end]
    indent = marker_line[: len(marker_line) - len(marker_line.lstrip())]
    card_lines = [
        indent + line if line else "" for line in build_card(project).splitlines()
    ]
    lines[end:end] = card_lines
    write_index(lines, content.endswith("\n"))
    return project


def card_lines_for(lines: list[str], marker_end: int, project: dict) -> list[str]:
    """Prépare les lignes indentées de la carte à insérer avant le marqueur END."""
    marker_line = lines[marker_end]
    indent = marker_line[: len(marker_line) - len(marker_line.lstrip())]
    return [
        indent + line if line else "" for line in build_card(project).splitlines()
    ]


def replace_card(data: dict) -> dict:
    """Remplace le bloc <article> d'origine, y compris si la section change."""
    project = normalize_project(data)
    if "start" not in data or "end" not in data:
        raise PortfolioError("Projet d'origine introuvable (start/end manquants).")

    content, lines = read_index()
    start = int(data["start"])
    end = int(data["end"])
    if not (0 <= start < end <= len(lines)):
        raise PortfolioError("Positions du projet invalides dans index.html.")

    source_size = None
    for size_value in SIZE_ORDER:
        marker_start, marker_end = get_markers(size_value, lines)
        if marker_start < start and end <= marker_end:
            source_size = size_value
            break
    if source_size is None:
        raise PortfolioError("Le bloc du projet est introuvable entre les marqueurs.")

    if source_size == project["size"]:
        lines[start:end] = card_lines_for(lines, end, project)
    else:
        del lines[start:end]
        _, target_end = get_markers(project["size"], lines)
        lines[target_end:target_end] = card_lines_for(lines, target_end, project)

    write_index(lines, content.endswith("\n"))
    return project


def remove_card(project: dict) -> None:
    """Supprime le bloc <article> choisi puis réécrit index.html."""
    content, lines = read_index()
    start, end = get_markers(project["size"], lines)
    project_start = int(project["start"])
    project_end = int(project["end"])

    if not (start < project_start < project_end <= end):
        raise PortfolioError("Positions du projet invalides dans index.html.")

    del lines[project_start:project_end]
    write_index(lines, content.endswith("\n"))


def describe(project: dict) -> str:
    """Prépare une ligne lisible pour les menus console."""
    parts = [project["name"]]
    if project["date"]:
        parts.append(project["date"])
    parts.append(CATEGORY_LABELS.get(project["category"], project["category"]))
    parts.append(LANGUAGE_LABELS.get(project["language"], project["language"]))
    return " · ".join(parts)
