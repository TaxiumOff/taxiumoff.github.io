# Portfolio d’Ilian Maanan

Un portfolio personnel simple et propre pour présenter mes projets : HTML, CSS et JavaScript natifs, **aucune dépendance**, aucun build requis.

## Lancer le site

Ouvre `index.html` dans ton navigateur.

Optionnel, pour servir le dossier localement :

```powershell
python -m http.server 8000
```

Puis va sur `http://localhost:8000`.

## Ajouter un projet

```powershell
python add_project.py
```

Le script pose les questions (type, nom, date, catégorie, langage, description, technologies, liens, style de vignette) et écrit directement la carte dans `index.html`, entre les marqueurs `BEGIN/END` de la bonne grille. Choisis `1` pour un **petit projet** ou `2` pour un **gros projet**, puis recharge la page.

## Structure

```text
index.html       Contenu et sections
css/style.css    Couleurs, mise en page, animations
js/main.js       Thème, menu, filtres, formulaire
add_project.py   Assistant console pour ajouter des projets
```

## Ce qu’il faut personnaliser

1. **Identité ✅** déjà renseignée pour Ilian Maanan : titre, initiales (`IM`), hero, « À propos » et pied de page.
2. **Tes projets** : lance `python add_project.py`. Il remplit `#projects-grid` (petits projets) ou `#projects-big-grid` (gros projets) selon ton choix. Ne supprime pas les marqueurs `BEGIN/END`. Tant qu’une grille est vide, un message d’attente s’affiche.
3. **Tes liens** : GitHub (`TaxiumOff`) et X (`taxiumoff`) sont déjà renseignés avec leurs logos SVG. Reste le `href="#"` de LinkedIn à remplacer.
4. **Ton e-mail ✅ à faire** : remplace `ton.email@example.com` dans `index.html` (lien `mailto:`) **et** dans `js/main.js` (`contactEmail`).
5. **Tes couleurs** : modifie les variables `--accent`, `--accent-2`, `--bg`… en haut de `css/style.css`. Le thème clair se règle juste en dessous (`[data-theme="light"]`).

## Ce qui est déjà en place

- Vignette de code personnalisée (`mood = "joyeux"`, `objectif = "progresser"`) avec coloration syntaxique
- Design responsive (mobile, tablette, desktop)
- Thème sombre / clair avec mémorisation du choix
- Animations d’apparition au défilement, effets au survol, fond animé
- Deux grilles : petits projets (vignettes compactes) et gros projets (grandes vignettes)
- Filtres imbriqués Catégorie → Langage avec « Tous » à chaque niveau et `aria-pressed`, synchronisés entre les deux grilles
- État vide automatique quand aucun projet n’est encore ajouté
- Formulaire qui ouvre l’application e-mail avec le message pré-rempli (aucun backend)
- Prise en charge de `prefers-reduced-motion` et navigation au clavier

## Aller plus loin

- Remplace la carte de code décorative par une capture d’écran ou une illustration.
- Branche un vrai formulaire via Formspree, Resend ou ton propre serveur.
- Ajoute une section « Expérience » ou « Blog » en copiant une section existante.
- Déploie sur GitHub Pages, Netlify ou Vercel.
