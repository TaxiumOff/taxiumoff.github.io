#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ajoute un projet (personnel ou majeur) au portfolio en écrivant dans index.html.

Usage : python add_project.py
Les cartes sont insérées entre les marqueurs BEGIN/END de chaque grille.
"""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"

MARKERS = {
    "petit": ("<!-- BEGIN SMALL PROJECTS -->", "<!-- END SMALL PROJECTS -->"),
    "gros": ("<!-- BEGIN BIG PROJECTS -->", "<!-- END BIG PROJECTS -->"),
}

SIZES = {
    "1": {"value": "petit", "label": "Projet personnel", "section": "Projets personnels"},
    "2": {"value": "gros", "label": "Projet majeur", "section": "Projets majeurs"},
}

CATEGORIES = {
    "1": {"value": "jeux-video", "label": "Jeux vidéo", "thumb": "thumb--one"},
    "2": {"value": "cybersecurite", "label": "Cybersécurité", "thumb": "thumb--two"},
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

THUMBS = {
    "1": "thumb--one",
    "2": "thumb--two",
    "3": "thumb--three",
}


def ask(label: str, default: str = "", required: bool = True) -> str:
    """Pose une question et renvoie la réponse (ou la valeur par défaut)."""
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"{label}{suffix} : ").strip()
        if not value and default:
            return default
        if value:
            return value
        if not required:
            return ""
        print("Ce champ est obligatoire.")


def ask_choice(label: str, choices: dict, default: str = "") -> dict:
    """Affiche un menu numéroté et renvoie l'élément choisi."""
    print(f"\n{label}")
    for key, item in choices.items():
        print(f"  {key} - {item['label']}")

    while True:
        raw = ask("Ton choix", default, required=False)
        if raw in choices:
            return choices[raw]
        if not raw and default in choices:
            return choices[default]
        print("Choix invalide, réessaie.")


def make_link(href: str, label: str, aria: str) -> str:
    """Construit un lien externe sécurisé, ou une chaîne vide si pas d'URL."""
    if not href:
        return ""
    safe_href = escape(href, quote=True)
    safe_aria = escape(aria, quote=True)
    return (
        f'<a href="{safe_href}" target="_blank" rel="noopener noreferrer" '
        f'aria-label="{safe_aria} (nouvel onglet)">'
        f'{label} <span aria-hidden="true">→</span></a>'
    )


def build_card(size, name, date, category, language, description, tags, demo, source, thumb) -> str:
    """Génère une vitrine pour un projet majeur, une carte compacte pour un projet personnel."""
    tag_items = "".join(
        f"<li>{escape(tag.strip())}</li>" for tag in tags.split(",") if tag.strip()
    )
    if not tag_items:
        tag_items = f"<li>{language['label']}</li>"

    links = [
        make_link(demo, "Voir le projet", f"Voir {name}"),
        make_link(source, "Code source", f"Code source de {name}"),
    ]
    links = "".join(link for link in links if link)
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

    if size["value"] == "gros":
        return f'''<article class="project-showcase reveal" data-category="{category["value"]}" data-language="{language["value"]}">
  <div class="project-showcase__visual {thumb}">
    <span class="project-card__badge">{category["label"]}</span>
    {lang_badge}
    <span class="project-showcase__index" aria-hidden="true"></span>
    <span class="project-showcase__title">{escape(name)}</span>
    <span class="project-card__arrow" aria-hidden="true">↗</span>
  </div>
  <div class="project-showcase__content">
    <p class="project-card__meta">{escape(date)} · {size["label"]}</p>
    <h3>{escape(name)}</h3>
    <p>{escape(description)}</p>
    <ul class="tags">{tag_items}</ul>
    <div class="project-card__footer">
      {links}
    </div>
  </div>
</article>'''

    return f'''<article class="project-card project-card--small reveal" data-category="{category["value"]}" data-language="{language["value"]}">
  <div class="project-card__thumb {thumb}">
    <span class="project-card__badge">{category["label"]}</span>
    {lang_badge}
    <span class="project-card__arrow" aria-hidden="true">↗</span>
  </div>
  <div class="project-card__body">
    <p class="project-card__meta">{escape(date)} · {size["label"]}</p>
    <h3>{escape(name)}</h3>
    <p>{escape(description)}</p>
    <ul class="tags">{tag_items}</ul>
  </div>
  <div class="project-card__footer">
    {links}
  </div>
</article>'''


def insert_card(size_value: str, card: str) -> None:
    """Insère la carte juste avant le marqueur END correspondant."""
    content = INDEX.read_text(encoding="utf-8")
    lines = content.splitlines()
    start, end = MARKERS[size_value]

    starts = [i for i, line in enumerate(lines) if line.strip() == start]
    ends = [i for i, line in enumerate(lines) if line.strip() == end]

    if not starts or not ends or ends[0] <= starts[0]:
        raise SystemExit(f"Marqueurs introuvables ou mal placés dans {INDEX.name}.")

    end_index = ends[0]
    marker_line = lines[end_index]
    indent = marker_line[: len(marker_line) - len(marker_line.lstrip())]

    card_lines = [indent + line if line else "" for line in card.splitlines()]
    lines[end_index:end_index] = card_lines

    trailing_newline = "\n" if content.endswith("\n") else ""
    INDEX.write_text("\n".join(lines) + trailing_newline, encoding="utf-8")


def main() -> None:
    print("=== Ajout d'un projet au portfolio ===")
    print(f"Fichier modifié : {INDEX}\n")

    size = ask_choice("Type de projet", SIZES, default="1")
    name = ask("Nom du projet")
    date = ask("Date de création (ex. 2026-11 ou novembre 2026)")
    category = ask_choice("Catégorie", CATEGORIES, default="1")
    language = ask_choice("Langage", LANGUAGES, default="1")
    description = ask("Description courte")
    tags = ask("Technologies (séparées par des virgules)", required=False)
    demo = ask("Lien de démonstration (Entrée = aucun)", required=False)
    source = ask("Lien du code source (Entrée = aucun)", required=False)

    default_thumb = "1" if category["value"] == "jeux-video" else "2"
    thumb_choice = ask(
        "Style de vignette : 1 (violet), 2 (vert) ou 3 (orange)", default_thumb
    )
    while thumb_choice not in THUMBS:
        print("Style invalide, choisis 1, 2 ou 3.")
        thumb_choice = ask("Style de vignette", default_thumb)
    thumb = THUMBS[thumb_choice]

    if not INDEX.exists():
        raise SystemExit(f"Introuvable : {INDEX}")

    card = build_card(
        size,
        name,
        date,
        category,
        language,
        description,
        tags,
        demo,
        source,
        thumb,
    )
    insert_card(size["value"], card)

    print(f"\n>>> {size['label']} « {name} » ajouté dans {INDEX.name} "
          f"(section {size['section']}).")
    print("Recharge la page pour le voir.")


if __name__ == "__main__":
    main()
