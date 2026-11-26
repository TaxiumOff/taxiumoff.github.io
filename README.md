# Portfolio — modèle vierge

Un point de départ simple et propre pour présenter tes projets : HTML, CSS et JavaScript natifs, **aucune dépendance**, aucun build requis.

## Lancer le site

Ouvre `index.html` dans ton navigateur.

Optionnel, pour servir le dossier localement :

```powershell
python -m http.server 8000
```

Puis va sur `http://localhost:8000`.

## Structure

```text
index.html      Contenu et sections (à compléter)
css/style.css   Couleurs, mise en page, animations
js/main.js      Thème, menu, filtres, formulaire
```

## Ce qu’il faut personnaliser

1. **Ton identité** dans `index.html` : nom, initiales (`brand__mark`), titre de la page, textes du hero et de la section « À propos ».
2. **Tes projets** : duplique un `<article class="project-card">`, change le texte, les liens et l’attribut `data-category` (`web`, `app` ou `experiment`) pour les filtres.
3. **Tes liens** : remplace tous les `href="#"` par tes profils GitHub, LinkedIn, X, etc.
4. **Ton e-mail** : dans `index.html` (lien `mailto:`) **et** dans `js/main.js` (`contactEmail`).
5. **Tes couleurs** : modifie les variables `--accent`, `--accent-2`, `--bg`… en haut de `css/style.css`. Le thème clair se règle juste en dessous (`[data-theme="light"]`).

## Ce qui est déjà en place

- Design responsive (mobile, tablette, desktop)
- Thème sombre / clair avec mémorisation du choix
- Animations d’apparition au défilement, effets au survol, fond animé
- Filtres de projets avec accessibilité (`aria-pressed`)
- Formulaire qui ouvre l’application e-mail avec le message pré-rempli (aucun backend)
- Prise en charge de `prefers-reduced-motion` et navigation au clavier

## Aller plus loin

- Remplace la carte de code décorative par une capture d’écran ou une illustration.
- Branche un vrai formulaire via Formspree, Resend ou ton propre serveur.
- Ajoute une section « Expérience » ou « Blog » en copiant une section existante.
- Déploie sur GitHub Pages, Netlify ou Vercel.
