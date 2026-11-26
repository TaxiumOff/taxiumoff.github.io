#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Application graphique pour gérer les projets du portfolio.

Usage : python project_manager.py

L'application détecte automatiquement les projets présents entre les marqueurs
de index.html et permet de les modifier, d'en ajouter ou d'en supprimer.
Tkinter est inclus dans Python : aucune dépendance à installer.
"""

import re
import shutil
import tkinter as tk
import unicodedata
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from portfolio_lib import (
    CATEGORIES,
    INDEX,
    LANGUAGES,
    PortfolioError,
    SIZE_VALUES,
    SIZES,
    SOURCE_DIR,
    THUMBS,
    describe,
    insert_card,
    load_projects,
    remove_card,
    replace_card,
)


def slugify(value: str) -> str:
    """Transforme un nom de projet en nom de dossier sûr."""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "projet"


class ProjectManager(tk.Tk):
    """Fenêtre principale de gestion des projets."""

    def __init__(self):
        super().__init__()
        self.title("Gestionnaire de projets — Portfolio Ilian Maanan")
        self.geometry("1000x680")
        self.minsize(860, 560)
        self.configure(padx=16, pady=12)

        self.projects = {}
        self.selected_key = None
        self.current_project = None
        self.status = tk.StringVar(value=INDEX.name)

        self.category_var = tk.StringVar(value="jeux-video")
        self.language_var = tk.StringVar(value="python")
        self.thumb_var = tk.StringVar(value="thumb--one")

        self._build_widgets()
        self.reload_projects()

    def _build_widgets(self) -> None:
        """Construit l'interface : liste à gauche, formulaire à droite."""
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        self._build_sidebar(main)
        self._build_form(main)

        status_bar = ttk.Label(
            self, textvariable=self.status, anchor="w", foreground="#6b7280"
        )
        status_bar.pack(fill="x", pady=(10, 0))

    def _build_sidebar(self, parent: ttk.Frame) -> None:
        sidebar = ttk.LabelFrame(parent, text="Projets détectés", padding=12)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        sidebar.columnconfigure(0, weight=1)
        sidebar.rowconfigure(2, weight=1)

        ttk.Button(
            sidebar, text="↻ Actualiser depuis index.html", command=self.reload_projects
        ).grid(row=0, column=0, sticky="ew")

        self.tree = ttk.Treeview(
            sidebar, columns=("name", "details"), show="tree headings", height=18
        )
        self.tree.heading("#0", text="Type")
        self.tree.heading("name", text="Projet")
        self.tree.heading("details", text="Détails")
        self.tree.column("#0", width=140, stretch=False)
        self.tree.column("name", width=170, stretch=True)
        self.tree.column("details", width=210, stretch=True)
        self.tree.grid(row=1, column=0, sticky="nsew", pady=(10, 8))
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        scrollbar = ttk.Scrollbar(
            sidebar, orient="vertical", command=self.tree.yview
        )
        scrollbar.grid(row=1, column=1, sticky="ns", pady=(10, 8))
        self.tree.configure(yscrollcommand=scrollbar.set)

        actions = ttk.Frame(sidebar)
        actions.grid(row=2, column=0, sticky="ew", pady=(4, 0))
        actions.columnconfigure(0, weight=1)
        actions.columnconfigure(1, weight=1)

        ttk.Button(actions, text="Nouveau projet", command=self.new_project).grid(
            row=0, column=0, sticky="ew", padx=(0, 4)
        )
        ttk.Button(actions, text="Supprimer", command=self.delete_project).grid(
            row=0, column=1, sticky="ew", padx=(4, 0)
        )

    def _build_form(self, parent: ttk.Frame) -> None:
        form_frame = ttk.LabelFrame(parent, text="Détails du projet", padding=14)
        form_frame.grid(row=0, column=1, sticky="nsew")
        form_frame.columnconfigure(1, weight=1)

        self.fields = {}
        rows = [
            ("name", "Nom du projet", True),
            ("date", "Date / repère", False),
            ("description", "Description", False),
            ("tags", "Technologies (séparées par des virgules)", False),
            ("demo", "Lien de démonstration", False),
            ("source", "Lien du code source", False),
            ("folder", "Dossier du code", False),
            ("code", "Fichier de code", False),
            ("report", "Rapport / description du code", False),
        ]

        for row, (key, label, required) in enumerate(rows):
            ttk.Label(form_frame, text=label).grid(
                row=row, column=0, sticky="nw", pady=(0, 10)
            )
            height = 5 if key == "description" else 6 if key == "report" else 1
            entry = (
                tk.Text(form_frame, height=height, wrap="word")
                if height > 1
                else ttk.Entry(form_frame)
            )
            entry.grid(row=row, column=1, sticky="ew", pady=(0, 10), padx=(10, 0))
            self.fields[key] = entry

            if key == "tags":
                ttk.Label(
                    form_frame,
                    text="Python, Tkinter, analyse de données",
                    foreground="#9ca3af",
                ).grid(row=row, column=2, sticky="w", padx=(6, 0))
            elif key == "folder":
                ttk.Label(
                    form_frame, text="source_code/", foreground="#9ca3af"
                ).grid(row=row, column=2, sticky="w", padx=(6, 0))
            elif key == "code":
                ttk.Button(
                    form_frame, text="Parcourir…", command=self.browse_code, width=12
                ).grid(row=row, column=2, sticky="w", padx=(6, 0))
            elif key == "report":
                ttk.Button(
                    form_frame, text="Choisir un README…", command=self.browse_readme, width=18
                ).grid(row=row, column=2, sticky="w", padx=(6, 0))
            elif required:
                ttk.Label(form_frame, text="*", foreground="#dc2626").grid(
                    row=row, column=2, sticky="w", padx=(4, 0)
                )

        options = ttk.Frame(form_frame)
        options.grid(row=len(rows), column=0, columnspan=3, sticky="ew", pady=(4, 14))
        options.columnconfigure(1, weight=1)
        options.columnconfigure(3, weight=1)
        options.columnconfigure(5, weight=1)

        ttk.Label(options, text="Section").grid(row=0, column=0, sticky="w")
        self.size_combo = ttk.Combobox(
            options,
            values=[SIZES[key]["label"] for key in ("1", "2")],
            state="readonly",
        )
        self.size_combo.current(0)
        self.size_combo.grid(row=0, column=1, sticky="ew", padx=(6, 18))

        ttk.Label(options, text="Catégorie").grid(row=0, column=2, sticky="w")
        self.category_combo = ttk.Combobox(
            options,
            values=[item["label"] for item in CATEGORIES.values()],
            textvariable=self.category_var,
            state="readonly",
        )
        self.category_combo.current(0)
        self.category_combo.grid(row=0, column=3, sticky="ew", padx=(6, 18))

        ttk.Label(options, text="Langage").grid(row=0, column=4, sticky="w")
        self.language_combo = ttk.Combobox(
            options,
            values=[item["label"] for item in LANGUAGES.values()],
            textvariable=self.language_var,
            state="readonly",
        )
        self.language_combo.current(0)
        self.language_combo.grid(row=0, column=5, sticky="ew", padx=(6, 0))

        ttk.Label(options, text="Vignette").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.thumb_combo = ttk.Combobox(
            options,
            values=[f"{info['number']} · {info['label']}" for info in THUMBS.values()],
            state="readonly",
        )
        self.thumb_combo.current(0)
        self.thumb_combo.grid(
            row=1, column=1, sticky="ew", pady=(10, 0), padx=(6, 18)
        )

        buttons = ttk.Frame(form_frame)
        buttons.grid(row=len(rows) + 1, column=0, columnspan=3, sticky="ew")
        buttons.columnconfigure(0, weight=1)
        buttons.columnconfigure(1, weight=1)

        self.save_button = ttk.Button(
            buttons, text="Enregistrer les modifications", command=self.save_project
        )
        self.save_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(buttons, text="Réinitialiser", command=self.reset_form).grid(
            row=0, column=1, sticky="ew", padx=(6, 0)
        )

    def reload_projects(self) -> None:
        """Relit index.html et recharge l'arborescence des projets."""
        try:
            self.projects = load_projects()
            self.selected_key = None
            self.current_project = None
            self.tree.delete(*self.tree.get_children())

            for size_value in ("petit", "gros"):
                size = SIZE_VALUES[size_value]
                parent = self.tree.insert(
                    "", "end", text=size["label"], values=("", ""), open=True
                )
                for number, project in enumerate(self.projects[size_value], 1):
                    key = f"{size_value}:{project['start']}:{project['end']}"
                    self.tree.insert(
                        parent,
                        "end",
                        iid=key,
                        text=f"{number:02d}",
                        values=(
                            project["name"],
                            describe(project).split(" · ", 1)[-1],
                        ),
                    )
                if not self.projects[size_value]:
                    self.tree.insert(
                        parent, "end", text="", values=("Aucun projet", ""), tags=("empty",)
                    )

            self.tree.tag_configure("empty", foreground="#9ca3af")
            self.new_project()
            self.status.set(f"{INDEX.name} chargé — {self.project_count()} projet(s) détecté(s)")
        except PortfolioError as error:
            messagebox.showerror("Lecture impossible", str(error))
            self.status.set(f"Erreur : {error}")

    def project_count(self) -> int:
        return sum(len(items) for items in self.projects.values())

    def new_project(self) -> None:
        """Prépare le formulaire pour la création d'un projet."""
        self.selected_key = None
        self.current_project = None
        self.tree.selection_remove(self.tree.selection())
        for key, widget in self.fields.items():
            self.set_field(key, "")
        self.size_combo.current(0)
        self.category_combo.current(0)
        self.language_combo.current(0)
        self.thumb_combo.current(0)
        self.save_button.configure(text="Créer le projet")
        self.status.set("Nouveau projet — les champs sont vides")

    def on_select(self, _event=None) -> None:
        """Charge le projet sélectionné dans le formulaire."""
        selection = self.tree.selection()
        if not selection:
            return
        key = selection[0]
        if ":" not in key:
            return

        project = self._find_project(key)
        if not project:
            return

        self.selected_key = key
        self.current_project = project
        for field in ("name", "date", "description", "tags", "demo", "source"):
            self.set_field(field, project.get(field, ""))

        folder = self._folder_from_project(project)
        self.set_field("folder", folder)
        self.set_field("code", project.get("code_file", ""))

        report = project.get("report_text", "")
        if not report and project.get("report_file"):
            report_path = INDEX.parent / project["report_file"]
            if report_path.exists():
                report = report_path.read_text(encoding="utf-8", errors="replace")
        self.set_field("report", report)

        size_key = next(
            key for key, item in SIZES.items() if item["value"] == project["size"]
        )
        self.size_combo.current(list(SIZES).index(size_key))

        category_key = next(
            key
            for key, item in CATEGORIES.items()
            if item["value"] == project["category"]
        )
        self.category_combo.current(list(CATEGORIES).index(category_key))
        self.category_var.set(CATEGORIES[category_key]["label"])

        language_key = next(
            key
            for key, item in LANGUAGES.items()
            if item["value"] == project["language"]
        )
        self.language_combo.current(list(LANGUAGES).index(language_key))
        self.language_var.set(LANGUAGES[language_key]["label"])

        thumb_key = THUMBS.get(project["thumb"], THUMBS["thumb--one"])
        self.thumb_combo.current(
            list(THUMBS).index(
                next(
                    key
                    for key, info in THUMBS.items()
                    if info["number"] == thumb_key["number"]
                )
            )
        )

        self.save_button.configure(text="Enregistrer les modifications")
        self.status.set(f"Édition de « {project['name']} »")

    def _folder_from_project(self, project: dict) -> str:
        """Retrouve le dossier source_code existant d'un projet."""
        for key in ("code_file", "report_file"):
            parts = project.get(key, "").split("/")
            if len(parts) >= 2 and parts[0] == "source_code":
                return parts[1]
        return slugify(project.get("name", ""))

    def _load_report_file(self, path: Path) -> None:
        """Charge un README dans le champ de rapport."""
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as error:
            messagebox.showerror("Lecture impossible", str(error))
            return
        self.set_field("report", text)
        if not self.get_field("folder"):
            self.set_field("folder", slugify(path.parent.name))
        self.status.set(f"Rapport chargé depuis {path.name}")

    def browse_code(self) -> None:
        """Choisis le fichier de code à copier dans source_code/<projet>."""
        path = filedialog.askopenfilename(
            title="Choisir le fichier de code",
            filetypes=[
                (
                    "Fichiers de code",
                    "*.py *.pyw *.cpp *.cc *.cxx *.c *.h *.hpp *.hh *.js *.ts *.html *.css *.txt",
                ),
                ("Tous les fichiers", "*.*"),
            ],
        )
        if not path:
            return

        source = Path(path)
        self.set_field("code", path)
        if not self.get_field("folder"):
            self.set_field("folder", slugify(self.get_field("name") or source.stem))

        readme = source.with_name("README.md")
        if readme.exists():
            self._load_report_file(readme)

        self.status.set(f"Fichier sélectionné : {source.name}")

    def browse_readme(self) -> None:
        """Choisis un README existant et le charge comme rapport."""
        path = filedialog.askopenfilename(
            title="Choisir un README",
            filetypes=[("Markdown / texte", "*.md *.txt"), ("Tous les fichiers", "*.*")],
        )
        if not path:
            return

        source = Path(path)
        self._load_report_file(source)
        if not self.get_field("code"):
            extensions = {".py", ".cpp", ".cc", ".cxx", ".c", ".h", ".hpp", ".js", ".ts"}
            candidates = [
                item
                for item in source.parent.iterdir()
                if item.is_file()
                and item.suffix.lower() in extensions
                and item.name.lower() != "readme.md"
            ]
            if candidates:
                self.set_field("code", str(candidates[0]))

    def _unique_folder(self, folder: str) -> str:
        """Évite qu'un dossier source soit partagé par deux projets."""
        used = set()
        for items in self.projects.values():
            for project in items:
                if project is self.current_project:
                    continue
                for key in ("code_file", "report_file"):
                    parts = project.get(key, "").split("/")
                    if len(parts) >= 2 and parts[0] == "source_code":
                        used.add(parts[1])

        if folder not in used:
            return folder
        for number in range(2, 100):
            candidate = f"{folder}-{number}"
            if candidate not in used:
                return candidate
        raise PortfolioError("Impossible de trouver un dossier source libre.")

    def prepare_assets(self, data: dict) -> None:
        """Copie le fichier de code et écrit le rapport dans source_code/."""
        folder = self._unique_folder(slugify(self.get_field("folder") or data["name"]))
        report_text = self.get_field("report")
        target_dir = SOURCE_DIR / folder

        code_field = self.get_field("code")
        if code_field:
            source = Path(code_field)
            if not source.is_absolute():
                source = INDEX.parent / source
            if not source.is_file():
                raise PortfolioError(f"Fichier de code introuvable : {source}")
            if source.resolve() != (target_dir / source.name).resolve():
                target_dir.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.copy2(source, target_dir / source.name)
                except OSError as error:
                    raise PortfolioError(f"Copie du code impossible : {error}")
            data["code_file"] = f"source_code/{folder}/{source.name}"
        else:
            data["code_file"] = ""

        if report_text:
            target_dir.mkdir(parents=True, exist_ok=True)
            try:
                (target_dir / "README.md").write_text(report_text, encoding="utf-8")
            except OSError as error:
                raise PortfolioError(f"Écriture du rapport impossible : {error}")
            data["report_file"] = f"source_code/{folder}/README.md"
            data["report_text"] = ""
        else:
            data["report_file"] = ""
            data["report_text"] = ""

        self.set_field("folder", folder)
        data["folder"] = folder

    def _find_project(self, key: str) -> dict | None:
        try:
            size_value, start, end = key.split(":")
            return next(
                (
                    project
                    for project in self.projects[size_value]
                    if project["start"] == int(start) and project["end"] == int(end)
                ),
                None,
            )
        except (KeyError, ValueError):
            return None

    def get_field(self, name: str) -> str:
        widget = self.fields[name]
        if isinstance(widget, tk.Text):
            return widget.get("1.0", "end-1c").strip()
        return widget.get().strip()

    def set_field(self, name: str, value: str) -> None:
        widget = self.fields[name]
        if isinstance(widget, tk.Text):
            widget.delete("1.0", "end")
            widget.insert("1.0", value)
        else:
            widget.delete(0, "end")
            widget.insert(0, value)

    def reset_form(self) -> None:
        """Recharge le projet sélectionné ou vide le formulaire."""
        if self.current_project:
            self.on_select()
        else:
            self.new_project()

    def read_form(self) -> dict:
        """Récupère les valeurs du formulaire sous forme de données propres."""
        size_label = self.size_combo.get()
        size_value = next(
            item["value"] for item in SIZES.values() if item["label"] == size_label
        )
        category_label = self.category_var.get()
        category_value = next(
            item["value"]
            for item in CATEGORIES.values()
            if item["label"] == category_label
        )
        language_label = self.language_var.get()
        language_value = next(
            item["value"]
            for item in LANGUAGES.values()
            if item["label"] == language_label
        )
        thumb_label = self.thumb_combo.get().split(" · ")[0]
        thumb_value = next(
            value for value, info in THUMBS.items() if info["number"] == thumb_label
        )

        data = {
            "size": size_value,
            "name": self.get_field("name"),
            "date": self.get_field("date"),
            "description": self.get_field("description"),
            "tags": self.get_field("tags"),
            "demo": self.get_field("demo"),
            "source": self.get_field("source"),
            "category": category_value,
            "language": language_value,
            "thumb": thumb_value,
            "folder": self.get_field("folder"),
            "code": self.get_field("code"),
            "report": self.get_field("report"),
            "code_file": self.current_project.get("code_file", "") if self.current_project else "",
            "report_file": self.current_project.get("report_file", "") if self.current_project else "",
            "report_text": self.get_field("report"),
        }
        if self.current_project:
            data["start"] = self.current_project["start"]
            data["end"] = self.current_project["end"]
        return data

    def save_project(self) -> None:
        """Crée ou met à jour le projet dans index.html."""
        try:
            data = self.read_form()
            if not data["name"]:
                raise PortfolioError("Le nom du projet est obligatoire.")
            self.prepare_assets(data)
            if self.current_project:
                project = replace_card(data)
                message = f"Projet « {project['name']} » mis à jour."
            else:
                project = insert_card(data)
                message = f"Projet « {project['name']} » créé."
            self.reload_projects()
            self.status.set(f"{message} Recharge la page pour le voir.")
        except PortfolioError as error:
            messagebox.showerror("Enregistrement impossible", str(error))
            self.status.set(f"Erreur : {error}")

    def delete_project(self) -> None:
        """Supprime le projet sélectionné après confirmation."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo(
                "Aucune sélection", "Sélectionne un projet dans la liste."
            )
            return
        key = selection[0]
        project = self._find_project(key)
        if not project:
            return

        confirm = messagebox.askyesno(
            "Supprimer le projet",
            f"Supprimer définitivement « {project['name']} » de {INDEX.name} ?",
            icon="warning",
        )
        if not confirm:
            return

        try:
            remove_card(project)
            self.reload_projects()
            self.status.set(
                f"Projet « {project['name']} » supprimé. Recharge la page pour le voir."
            )
        except PortfolioError as error:
            messagebox.showerror("Suppression impossible", str(error))
            self.status.set(f"Erreur : {error}")


def main() -> None:
    app = ProjectManager()
    app.mainloop()


if __name__ == "__main__":
    main()
