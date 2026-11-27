# Portfolio d’Ilian Maanan

Site statique en HTML, CSS et JavaScript natifs. Aucune dépendance, aucun build, aucune donnée personnelle exposée.

## Lancer le site

```powershell
python -m http.server 8000
```

Puis ouvrir `http://localhost:8000`. `index.html` fonctionne aussi directement en `file://`.

## Contenu

- **Projets majeurs** : présentés en vitrine, avec contexte, choix techniques et liens.
- **Projets personnels** : grille compacte, filtrable par catégorie (jeux vidéo / cybersécurité) et par langage (Python / C++).
- **À propos** et **contact** : formulaire qui ouvre l’application e-mail avec le message pré-rempli, au vouvoiement.

Les fiches sont dans `projects/`, une page par projet. Les liens GitHub, l’archive ZIP et l’exécutable sont construits à partir du dépôt public renseigné pour chaque projet : aucun fichier source n’est hébergé sur le site.

Un fichier choisi dans le dépôt public peut être affiché sur la fiche sous forme d’aperçu de code, en lecture seule : barre de fenêtre, coloration des mots-clés, chaînes et commentaires.

## Structure

```text
index.html        Accueil
css/style.css     Thème clair/sombre, mise en page, fiches, blocs de code
js/site.js        Thème, menu mobile, filtres, formulaire de contact
projects/         Fiches publiées, une par projet
```

## Personnaliser

1. L’adresse `ilianmaanan.pro@gmail.com` est déjà renseignée dans `index.html` et `contactEmail` dans `js/site.js`.
2. Renseigner les projets réels dans les fiches, sans inventer de contenu.
3. Ajuster les couleurs via les variables en haut de `css/style.css` : six teintes de vignette sont disponibles.

Les profils GitHub (`TaxiumOff`) et X (`taxiumoff`) sont déjà renseignés.

## Vérifications utiles

```powershell
node --check js/site.js
git status --short
```

Le push reste à faire par l’utilisateur.
