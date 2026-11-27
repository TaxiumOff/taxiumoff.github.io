# Ilian Maanan — Portfolio

Je m’appelle Ilian Maanan. Je suis en classe de première générale et je développe mes compétences en programmation, avec un intérêt particulier pour le développement de jeux vidéo et la cybersécurité.

Je travaille avec Python, les bases de l’algorithmique, la création de jeux et la sécurité informatique. Passionné par la technologie et l’informatique depuis ma plus tendre enfance, j’aime relever des défis techniques et apprendre de nouvelles compétences. La licence *The Legend of Zelda* a bercé mon enfance et m’a donné envie de créer mes propres jeux vidéo.

Site statique en HTML, CSS et JavaScript natifs. Aucune dépendance, aucun build, aucune donnée sensible exposée.

## Lancer le site

```powershell
python -m http.server 8000
```

Puis ouvrir `http://localhost:8000`. `index.html` fonctionne aussi directement en `file://`.

## Contenu

- **Projets majeurs** : présentés en vitrine, avec contexte, choix techniques et liens.
- **Projets personnels** : grille compacte, filtrable par catégorie (jeux vidéo / cybersécurité) et par langage (Python / C++). Le premier projet publié est **Juste Prix**, mon premier jeu en C++ (2026).
- **À propos** : profil, domaines de travail et parcours.
- **Contact** : formulaire qui ouvre l’application e-mail avec le message pré-rempli, au vouvoiement.

Les fiches sont dans `projects/`, une page par projet. Les liens GitHub, l’archive ZIP et l’exécutable sont construits à partir du dépôt public renseigné pour chaque projet : aucun fichier source n’est hébergé sur le site.

Un fichier choisi dans le dépôt public peut être affiché sur la fiche sous forme d’aperçu de code, en lecture seule : barre de fenêtre, coloration des mots-clés, chaînes et commentaires.

## Profils et contact

- E-mail : `ilianmaanan.pro@gmail.com`
- GitHub : [TaxiumOff](https://github.com/TaxiumOff)
- X : [taxiumoff](https://x.com/taxiumoff)

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

Les profils GitHub (`TaxiumOff`) et X (`taxiumoff`) sont déjà renseignés dans le site.

## Vérifications utiles

```powershell
node --check js/site.js
git status --short
```

Le push reste à faire par l’utilisateur.
