#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Supprime un projet du portfolio en retirant sa carte de index.html.

Usage : python remove_project.py
Les cartes sont repérées entre les marqueurs BEGIN/END de chaque grille.
"""

from portfolio_lib import (
    INDEX,
    PortfolioError,
    SIZES,
    describe,
    load_projects,
    remove_card,
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


def main() -> None:
    print("=== Suppression d'un projet du portfolio ===")
    print(f"Fichier modifié : {INDEX}\n")

    try:
        size = ask_choice("Type de projet", SIZES)
        projects = load_projects()[size["value"]]
    except PortfolioError as error:
        raise SystemExit(f"Erreur : {error}")

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

    try:
        remove_card(selected)
    except PortfolioError as error:
        raise SystemExit(f"Erreur : {error}")

    print(f"\n>>> {size['label']} « {selected['name']} » supprimé de {INDEX.name}.")
    print("Recharge la page pour voir le résultat.")


if __name__ == "__main__":
    main()
