# Portfolio d’Ilian Maanan

Un portfolio personnel simple et propre pour présenter mes projets : HTML, CSS et JavaScript natifs, **aucune dépendance**, aucun build requis.

## Lancer le site

Ouvre `index.html` dans ton navigateur.

Optionnel, pour servir le dossier localement :

```powershell
python -m http.server 8000
```

Puis va sur `http://localhost:8000`.

## Structure

```text
index.html      Contenu et sections
css/style.css   Couleurs, mise en page, animations
js/main.js      Thème, menu, filtres, formulaire
```

## Ce qu’il faut personnaliser

1. **Identité ✅** déjà renseignée pour Ilian Maanan : titre, initiales (`IM`), hero, « À propos » et pied de page.
2. **Tes projets** : dans `#projects-grid`, duplique le modèle laissé en commentaire. Renseigne `data-category` (`jeux-video` ou `cybersecurite`) et `data-language` (`python` ou `cpp`), puis adapte le badge, le badge de langage (`lang-python` / `lang-cpp`) et le texte. Tant qu’il n’y a aucune carte, un message d’attente s’affiche.
3. **Tes liens** : GitHub pointe déjà vers `taxiumoff`. Remplace les `href="#"` restants (X, LinkedIn) par tes profils.
4. **Ton e-mail ✅ à faire** : remplace `ton.email@example.com` dans `index.html` (lien `mailto:`) **et** dans `js/main.js` (`contactEmail`).
5. **Tes couleurs** : modifie les variables `--accent`, `--accent-2`, `--bg`… en haut de `css/style.css`. Le thème clair se règle juste en dessous (`[data-theme="light"]`).

## Ce qui est déjà en place

- Vignette de code personnalisée (`mood = "joyeux"`, `objectif = "progresser"`) avec coloration syntaxique
- Design responsive (mobile, tablette, desktop)
- Thème sombre / clair avec mémorisation du choix
- Animations d’apparition au défilement, effets au survol, fond animé
- Filtres imbriqués Catégorie → Langage avec « Tous » à chaque niveau et `aria-pressed`
- État vide automatique quand aucun projet n’est encore ajouté
- Formulaire qui ouvre l’application e-mail avec le message pré-rempli (aucun backend)
- Prise en charge de `prefers-reduced-motion` et navigation au clavier

## Aller plus loin

- Remplace la carte de code décorative par une capture d’écran ou une illustration.
- Branche un vrai formulaire via Formspree, Resend ou ton propre serveur.
- Ajoute une section « Expérience » ou « Blog » en copiant une section existante.
- Déploie sur GitHub Pages, Netlify ou Vercel.
