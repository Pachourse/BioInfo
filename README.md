---
title : "README - projet de BioInfo"
author : ["Paviel Schertzer"]
---

# Projet de BioInfo

[TOC]

## Architecture du projet

```txt
.
├── AUTHORS
├── README.md
├── src
│   ├── bw-build.py
│   └── bw-search.py
├── test.cmv.fasta.idx
└── tests
    ├── brouillon.ipynb
    ├── check_compressed_sequence.py
    ├── method2.py
    └── tests.py
```

### Requirements

### Autres ressources supplémentaires

Un dossier `/tests` contient une test suit qui génère et execute une commande permettant d'executer le programme `bw-build` et `bw-search` les différents fichiers de data. 

## Travail effectué

### Partie 1

La partie 1 a une approche un peu différente de celle proposée par le second article conseillé en sources. L'implémentation de la partie 1 suit le fonctionnement classique de la Transformée de Burrows-Wheeler. 

```txt
┌────────┐  ┌────────┐  ┌─┐
│BANANA$ │  │$BANANA │  │A│
│$BANANA │  │A$BANAN │  │N│
│A$BANAN │  │ANA$BAN │  │N│
│NA$BANA │─▶│ANANA$B │─▶│B│
│ANA$BAN │  │BANANA$ │  │$│
│NANA$BA │  │NA$BANA │  │A│
│ANANA$B │  │NANA$BA │  │A│
└────────┘  └────────┘  └─┘
```

Avec les indexes :

```
┌────────┐  ┌────────┐  ┌───┐
│1234560 │  │0123456 │  │   │
│BANANA$ │  │$BANANA │  │A 6│
│        │  │        │  │   │
│0123456 │  │6012345 │  │   │
│$BANANA │  │A$BANAN │  │N 5│
│        │  │        │  │   │
│6012345 │  │4560123 │  │   │
│A$BANAN │  │ANA$BAN │  │N 3│
│        │  │        │  │   │
│5601234 │  │2345601 │  │   │
│NA$BANA │─▶│ANANA$B │─▶│B 1│
│        │  │        │  │   │
│4560123 │  │1234560 │  │   │
│ANA$BAN │  │BANANA$ │  │$ 0│
│        │  │        │  │   │
│3456012 │  │5601234 │  │   │
│NANA$BA │  │NA$BANA │  │A 4│
│        │  │        │  │   │
│2345601 │  │3456012 │  │   │
│ANANA$B │  │NANA$BA │  │A 2|
└────────┘  └────────┘  └───┘
```



L'approche retenue sera cependant un peu différente sur les indexes et la position du caractère `$`en raison d'une mauvaise interprétation de l'article de [wikipedia](https://fr.wikipedia.org/wiki/Transformée_de_Burrows-Wheeler). 

L'erreur de lecture, par l'absence de `$` dans l'exemple et la présence d'une lettre en rouge, 

