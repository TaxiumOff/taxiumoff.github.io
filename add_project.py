#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ajoute un projet (personnel ou majeur) au portfolio en écrivant dans index.html.

Usage : python add_project.py
Les cartes sont insérées entre les marqueurs BEGIN/END de chaque grille.
"""

from portfolio_lib import (
    CATEGORIES,
    DEFAULT_THUMBS,
    INDEX,
    LANGUAGES,
    PortfolioError,
    SIZES,
    THUMBS,
    insert_card,
)


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

    default_thumb = THUMBS[DEFAULT_THUMBS[category["value"]]]["number"]
    thumb_choice = ask(
        "Style de vignette : 1 (violet), 2 (vert) ou 3 (orange)", default_thumb
    )
    while thumb_choice not in {"1", "2", "3"}:
        print("Style invalide, choisis 1, 2 ou 3.")
        thumb_choice = ask("Style de vignette", default_thumb)
    thumb = next(
        value for value, info in THUMBS.items() if info["number"] == thumb_choice
    )

    try:
        insert_card(
            {
                "size": size["value"],
                "name": name,
                "date": date,
                "category": category["value"],
                "language": language["value"],
                "description": description,
                "tags": tags,
                "demo": demo,
                "source": source,
                "thumb": thumb,
            }
        )
    except PortfolioError as error:
        raise SystemExit(f"Erreur : {error}")

    print(f"\n>>> {size['label']} « {name} » ajouté dans {INDEX.name} "
          f"(section {size['section']}).")
    print("Recharge la page pour le voir.")


if __name__ == "__main__":
    main()
