#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Supprime un projet du portfolio en retirant sa carte de index.html.

Usage : python remove_project.py
Les cartes sont repérées entre les marqueurs BEGIN/END de chaque grille.
"""

import re
from html import unescape
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

CATEGORY_LABELS = {
    "jeux-video": "Jeux vidéo",
    "cybersecurite": "Cybersécurité",
}

LANGUAGE_LABELS = {
    "python": "Python",
    "cpp": "C++",
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


def ask_choice(label: str, choices: dict, default: str = "1") -> dict:
    """Affiche un menu numéroté et renvoie l'élément choisi."""
    print(f"\n{label}")
    for key, item in choices.items():
        print(f"  {key} - {item['label']}")

    while True:
        raw = ask("Ton choix", default, required=False)
        if raw in choices:
            return choices[raw]
        print("Choix invalide, réessaie.")


def clean_text(fragment: str) -> str:
    """Retire les balises d'un fragment HTML et décode les entités."""
    text = re.sub(r"<[^>]+>", " ", fragment)
    return " ".join(unescape(text).split())


def read_attribute(block: str, name: str) -> str:
    """Lit un attribut data-* sur la balise <article> du projet."""
    match = re.search(rf'{name}="([^"]*)"', block)
    return match.group(1) if match else ""


def parse_projects(lines: list, start: int, end: int) -> list:
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
            raise SystemExit("Bloc de projet non fermé : vérifie index.html.")

        block = "\n".join(block_lines)

        title = re.search(
            r'<span class="project-showcase__title"[^>]*>(.*?)</span>', block, re.S
        )
        name = clean_text(title.group(1)) if title else ""
        if not name:
            heading = re.search(r"<h3[^>]*>(.*?)</h3>", block, re.S)
            name = clean_text(heading.group(1)) if heading else ""
        if not name:
            name = "Sans nom"

        meta = re.search(r'<p class="project-card__meta"[^>]*>(.*?)</p>', block, re.S)
        meta_text = clean_text(meta.group(1)) if meta else ""
        date = meta_text.split("·")[0].strip() if "·" in meta_text else meta_text

        category_value = read_attribute(block, "data-category")
        language_value = read_attribute(block, "data-language")

        projects.append(
            {
                "start": block_start,
                "end": index,
                "name": name,
                "date": date,
                "category": CATEGORY_LABELS.get(category_value, category_value or "—"),
                "language": LANGUAGE_LABELS.get(language_value, language_value or "—"),
            }
        )

    return projects


def describe(project: dict) -> str:
    """Prépare une ligne lisible pour le menu de suppression."""
    parts = [project["name"]]
    if project["date"]:
        parts.append(project["date"])
    parts.append(project["category"])
    parts.append(project["language"])
    return " · ".join(parts)


def get_markers(size_value: str, lines: list) -> tuple:
    """Renvoie les indices des marqueurs BEGIN/END pour le type demandé."""
    begin, end = MARKERS[size_value]
    starts = [i for i, line in enumerate(lines) if line.strip() == begin]
    ends = [i for i, line in enumerate(lines) if line.strip() == end]

    if not starts or not ends or ends[0] <= starts[0]:
        raise SystemExit(f"Marqueurs introuvables ou mal placés dans {INDEX.name}.")

    return starts[0], ends[0]


def remove_project(lines: list, start: int, end: int, project: dict, content: str) -> None:
    """Supprime le bloc choisi puis réécrit index.html."""
    region = lines[start + 1 : end]
    relative_start = project["start"] - (start + 1)
    relative_end = project["end"] - (start + 1)

    del region[relative_start:relative_end]
    lines[start + 1 : end] = region

    trailing_newline = "\n" if content.endswith("\n") else ""
    INDEX.write_text("\n".join(lines) + trailing_newline, encoding="utf-8")


def main() -> None:
    print("=== Suppression d'un projet du portfolio ===")
    print(f"Fichier modifié : {INDEX}\n")

    if not INDEX.exists():
        raise SystemExit(f"Introuvable : {INDEX}")

    size = ask_choice("Type de projet", SIZES)
    content = INDEX.read_text(encoding="utf-8")
    lines = content.splitlines()
    start, end = get_markers(size["value"], lines)
    projects = parse_projects(lines, start, end)

    if not projects:
        print(f"\nAucun projet à supprimer dans « {size['section']} ».")
        return

    print(f"\n{size['section']} ({len(projects)}) :")
    for number, project in enumerate(projects, 1):
        print(f"  {number} - {describe(project)}")

    raw = ask(
        "\nNuméro ou nom exact du projet à supprimer (Entrée = annuler)",
        required=False,
    )
    if not raw:
        print("Annulation : aucun fichier modifié.")
        return

    selected = None
    if raw.isdigit():
        number = int(raw)
        if 1 <= number <= len(projects):
            selected = projects[number - 1]
        else:
            print("Numéro invalide : aucun fichier modifié.")
            return
    else:
        matches = [p for p in projects if p["name"].casefold() == raw.casefold()]
        if not matches:
            print("Projet introuvable : aucun fichier modifié.")
            return
        if len(matches) > 1:
            print("Plusieurs projets portent ce nom : utilise le numéro.")
            return
        selected = matches[0]

    confirmation = ask(
        f"Supprimer « {selected['name']} » ? (o/n)", default="n", required=False
    )
    if confirmation.casefold() not in {"o", "oui"}:
        print("Annulation : aucun fichier modifié.")
        return

    remove_project(lines, start, end, selected, content)

    print(f"\n>>> {size['label']} « {selected['name']} » supprimé de {INDEX.name}.")
    print("Recharge la page pour voir le résultat.")


if __name__ == "__main__":
    main()
