# Portfolio d’Ilian Maanan

Un portfolio personnel simple et propre pour présenter mes projets : HTML, CSS et JavaScript natifs, **aucune dépendance**, aucun build requis.

## Lancer le site

Ouvre `index.html` dans ton navigateur.

Optionnel, pour servir le dossier localement :

```powershell
python -m http.server 8000
```

Puis va sur `http://localhost:8000`.

## Gérer les projets avec l’application graphique

```powershell
python project_manager.py
```

L’application détecte automatiquement les projets déjà présents dans `index.html` et les affiche dans la liste de gauche. Sélectionne un projet pour modifier son nom, sa date, sa description, ses technologies, ses liens, sa catégorie, son langage, sa vignette ou sa section, puis clique sur **Enregistrer les modifications**. Le bouton **Nouveau projet** crée une carte, et **Supprimer** retire la carte choisie après confirmation. Aucun projet n’est inventé par l’application : elle ne travaille que sur le contenu existant de `index.html`.

Pour joindre le code d’un projet :

1. Renseigne le **Dossier du code** (par défaut, une version simplifiée du nom du projet).
2. Clique sur **Parcourir…** dans **Fichier de code** : le fichier est copié dans `source_code/[dossier]/`.
3. Écris ton rapport directement dans **Rapport / description du code**, ou clique sur **Choisir un README…** pour charger un `README.md` existant. Le contenu est enregistré dans `source_code/[dossier]/README.md`.

Sur le site, chaque projet concerné affiche un panneau **Voir le code et le rapport** : le code est coloré selon son langage (Python, C/C++, JavaScript), numéroté et affiché en lecture seule. Il faut servir le dossier avec `python -m http.server 8000` pour que les fichiers `source_code/` soient accessibles au navigateur.

Tkinter est inclus dans Python : aucune installation supplémentaire n’est nécessaire. Recharge le navigateur après chaque enregistrement.

## Ajouter un projet depuis la console

```powershell
python add_project.py
```

Le script pose les questions (type, nom, date, catégorie, langage, description, technologies, liens, style de vignette) et écrit directement la carte dans `index.html`, entre les marqueurs `BEGIN/END` de la bonne grille. Choisis `1` pour un **projet personnel** (carte compacte avec icône de langage) ou `2` pour un **projet majeur** (présentation en vitrine, sans filtre), puis recharge la page.

## Supprimer un projet depuis la console

```powershell
python remove_project.py
```

Le script liste les projets du type choisi, demande le **numéro ou le nom exact**, puis une confirmation. Il retire uniquement le bloc `<article>` correspondant et laisse les marqueurs `BEGIN/END` en place.

## Structure

```text
index.html         Contenu et sections
css/style.css      Couleurs, mise en page, animations, lecteur de code
js/main.js         Thème, menu, filtres, lecteur de code, formulaire
project_manager.py Application graphique pour gérer les projets
portfolio_lib.py   Fonctions partagées de lecture et d'écriture des cartes
add_project.py     Assistant console pour ajouter des projets
remove_project.py  Assistant console pour supprimer un projet
source_code/       Fichiers de code et README, classés par projet
```

## Ce qu’il faut personnaliser

1. **Identité ✅** déjà renseignée pour Ilian Maanan : titre, initiales (`IM`), hero, « À propos » et pied de page.
2. **Tes projets** : lance `python project_manager.py` pour créer, modifier ou supprimer des cartes dans `#projects-personal-grid` (projets personnels) et `#projects-major-grid` (projets majeurs). Tu peux aussi joindre un fichier de code et un rapport, stockés dans `source_code/[nom_du_projet]/`. Les scripts `add_project.py` et `remove_project.py` restent disponibles en console. Ne supprime pas les marqueurs `BEGIN/END`. Tant qu’une grille est vide, un message d’attente s’affiche.
3. **Tes liens** : GitHub (`TaxiumOff`) et X (`taxiumoff`) sont déjà renseignés avec leurs logos SVG. Reste le `href="#"` de LinkedIn à remplacer.
4. **Adresse e-mail ✅ à faire** : remplace `ton.email@example.com` dans `index.html` (lien `mailto:`) **et** dans `js/main.js` (`contactEmail`).
5. **Tes couleurs** : modifie les variables `--accent`, `--accent-2`, `--bg`… en haut de `css/style.css`. Le thème clair se règle juste en dessous (`[data-theme="light"]`).

## Ce qui est déjà en place

- Vignette de code personnalisée (`mood = "motivé"`, `objectif = "progresser"`) avec coloration syntaxique
- Design responsive (mobile, tablette, desktop)
- Thème sombre / clair avec mémorisation du choix
- Animations d’apparition au défilement, effets au survol, fond animé
- Projets majeurs en vitrine (grand visuel + contenu, numérotation automatique, pas de filtre) placés avant les projets personnels
- Projets personnels en bas de page : vignettes compactes, badges avec l’icône du langage et son texte
- Filtres Catégorie → Langage avec « Tous » à chaque niveau et `aria-pressed`, uniquement sur les projets personnels
- Vocabulaire et messages d’attente professionnels : aucune référence à l’outil d’ajout dans la partie visible du site
- Lecteur de code intégré aux cartes : coloration Python/C++/JavaScript, numéros de ligne et affichage en lecture seule
- Application graphique Tkinter pour détecter et gérer les projets sans éditer le HTML à la main
- Outils console pour ajouter et supprimer un projet sans éditer le HTML à la main
- État vide automatique quand aucune carte n’est présente
- Formulaire qui ouvre l’application e-mail avec le message pré-rempli (aucun backend)
- Prise en charge de `prefers-reduced-motion` et navigation au clavier

## Aller plus loin

- Remplace la carte de code décorative par une capture d’écran ou une illustration.
- Branche un vrai formulaire via Formspree, Resend ou ton propre serveur.
- Ajoute une section « Expérience » ou « Blog » en copiant une section existante.
- Déploie sur GitHub Pages, Netlify ou Vercel.