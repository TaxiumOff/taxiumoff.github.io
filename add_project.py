#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ajoute un projet (petit ou gros) au portfolio en écrivant dans index.html.

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
    "1": {"value": "petit", "label": "Petit projet", "section": "Petits projets"},
    "2": {"value": "gros", "label": "Gros projet", "section": "Gros projets"},
}

CATEGORIES = {
    "1": {"value": "jeux-video", "label": "Jeux vidéo", "thumb": "thumb--one"},
    "2": {"value": "cybersecurite", "label": "Cybersécurité", "thumb": "thumb--two"},
}

LANGUAGES = {
    "1": {"value": "python", "label": "Python", "badge": "lang-python"},
    "2": {"value": "cpp", "label": "C++", "badge": "lang-cpp"},
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
    """Génère le HTML d'une carte projet."""
    size_class = "project-card--big" if size["value"] == "gros" else "project-card--small"

    cover = ""
    if size["value"] == "gros":
        cover = f'    <span class="project-card__cover">{escape(name)}</span>\n'

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

    return f'''<article class="project-card {size_class} reveal" data-category="{category["value"]}" data-language="{language["value"]}">
  <div class="project-card__thumb {thumb}">
    <span class="project-card__badge">{category["label"]}</span>
    <span class="project-card__lang {language["badge"]}">{language["label"]}</span>
{cover}    <span class="project-card__arrow" aria-hidden="true">↗</span>
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
