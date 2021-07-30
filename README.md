---

title : "README - projet de BioInfo"
author : ["Paviel Schertzer"]

---

# Projet de BioInfo

## Architecture du projet

Le projet suit l’architecture exigée par les consignes mais rajoute deux parties : 

- un répertoire `tests/` concernant des pistes de recherche et des tests unitaires
- un `README.md` contenant des explications concernant certains choix et pistes de recherche en plus des requirements et des consignes d’execution demandés dans le sujet. 
- un fichier `requirements.txt` pour pouvoir installer automatiquement les modules pip nécessaires si vous souhaitez executer les programmes dans un environemment virtuel de travail. 

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

```txt
AJOUTER ICI REQUIREMENTS
```

### Autres ressources supplémentaires

#### Tests

Un dossier `/tests` contient une test suit qui génère et execute une commande permettant d'executer le programme `bw-build` et `bw-search` les différents fichiers de data. 

Les tests sont executables dans le dissier `tests/` avec la présence du dossier `data/` en amont du projet. Ces paramètres sont modifiables ne haut du projet. 

## Travail effectué

### Partie 1

La partie 1 a une approche un peu différente de celle proposée par le second article conseillé en sources. L'implémentation de la partie 1 suit le fonctionnement classique de la Transformée de Burrows-Wheeler. 

```txt
┌─────────┐  ┌─────────┐  ┌─┐
│ BANANA$ │  │ $BANANA │  │A│
│ $BANANA │  │ A$BANAN │  │N│
│ A$BANAN │  │ ANA$BAN │  │N│
│ NA$BANA │─▶│ ANANA$B │─▶│B│
│ ANA$BAN │  │ BANANA$ │  │$│
│ NANA$BA │  │ NA$BANA │  │A│
│ ANANA$B │  │ NANA$BA │  │A│
└─────────┘  └─────────┘  └─┘
```

Avec les indexes :

```txt
┌─────────┐  ┌───────────┐  ┌───┐
│ 1234560 │  │ 012345[6] │  │   │
│ BANANA$ │  │ $BANAN[A] │  │A 6│
│         │  │           │  │   │
│ 0123456 │  │ 601234[5] │  │   │
│ $BANANA │  │ A$BANA[N] │  │N 5│
│         │  │           │  │   │
│ 6012345 │  │ 456012[3] │  │   │
│ A$BANAN │  │ ANA$BA[N] │  │N 3│
│         │  │           │  │   │
│ 5601234 │  │ 234560[1] │  │   │
│ NA$BANA │─▶│ ANANA$[B] │─▶│B 1│
│         │  │           │  │   │
│ 4560123 │  │ 123456[0] │  │   │
│ ANA$BAN │  │ BANANA[$] │  │$ 0│
│         │  │           │  │   │
│ 3456012 │  │ 560123[4] │  │   │
│ NANA$BA │  │ NA$BAN[A] │  │A 4│
│         │  │           │  │   │
│ 2345601 │  │ 345601[2] │  │   │
│ ANANA$B │  │ NANA$B[A] │  │A 2|
└─────────┘  └───────────┘  └───┘
```



L'approche retenue sera cependant un peu différente sur les indexes et la position du caractère `$`en raison d'une mauvaise interprétation de l'article de [wikipedia](https://fr.wikipedia.org/wiki/Transformée_de_Burrows-Wheeler). 

L'erreur de lecture, par l'absence de `$` dans l'exemple et la présence d'une lettre en rouge, j'ai tout bonnement eu l'idée de le mettre à gauche et non à droite, et d'indexer les lignes et non les colonnes. 

```txt
┌─────────┐  ┌─────────┐  ┌─┐
│$BANANA 0│  │$BANANA 0│  │A│ 6 - 0 = 6
│A$BANAN 1│  │A$BANAN 1│  │N│ 6 - 1 = 5
│NA$BANA 2│  │ANA$BAN 3│  │N│ 6 - 3 = 3
│ANA$BAN 3│─▶│ANANA$B 5│─▶│B│ 6 - 5 = 1
│NANA$BA 4│  │BANANA$ 6│  │$│ 6 - 6 = 0
│ANANA$B 5│  │NA$BANA 2│  │A│ 6 - 2 = 4
│BANANA$ 6│  │NANA$BA 4│  │A│ 6 - 4 = 2
└─────────┘  └─────────┘  └─┘
```

On remarquera une erreur dans les indexes, cependant simple à corriger : il suffit de faire `index = len(banana) - index` avant l'affichage du résultat. Nous pouvons aussi remarque que dans le code l'indexe débute à 1 : c'est une mauvaise interprétation du sujet avec $n > 1$. Cette erreur est corrigée à ce même moment de soustraction. 

Cette erreur est cependant un attout sur l’utilisation de la mémoire : une seconde implémentation plus classique est disponible dans `tests/method2.py`. Le paramètre booléen `methode1` permet de choisir la méthode 1 précédammanet décrite ou la 2 plus classique. 

À noter que cette seconde méthode n’est pas réellement optimisée mais me semblait obligatoire pour approcher la 3ème partie. L’un de ses principaux défauts est la concaténation des lettres de la séquence en une string pour pouvoir assurer le tri sans problème sur le premier paramètre du tuple `([sequence], [indexe])`. 

Dès la découverte de cette approche spécifique du premier programme, la création du second débuta avec un questionnement sur le plan théorique de l’avantage du premier suivi d’un essai pratique. 

**Raisonnement théorique :**

Pour une séquence de taille $n$ devenue $n+ 1$ avec l’ajout du `$`, la première méthode ne stoque d’un seul tableau contenant les différents indexes présents en sortie : donc de taille $n+1$. En ordonnant les séquences de longueur $n + 1$ avec le`$` par ordre alphabérique nous obtenons un matrice de taille $(n+1)$ de large et $(n+1)$ de haut pour les séquences et $(n + 1), (n)$ pour les indexes pendnat les opérations. Nous avons donc une matrice de taille : $(n+ 2, n+1)$. 

Pour la seconde méthode nous avons une matrice $(n+1),(n+1)$ pour les séquences et $(n+1), (n+1)$ pour les indexes (car un array par séquence). 

Donc la méthode 1 semble être plus intéressante au niveau de la taille des matrices pour les opérations. 

> remarque : ces dimensions ne sont pas réellement réelles, on passe souvent d’array à string mais dans l’idée elles sont justes

**Vérification pratique :**

Une vérification peut être menée par le programme `tests/methode2.py` en modifiant le paramètre `methode1 = False` à `True` en fonction de la méthode désirée. 

Un code trouvé sur [stack overflow](https://stackoverflow.com/questions/11886862/calculating-computational-time-and-memory-for-a-code-in-python) permet de log la mémoire utilisée. 

```python3
import time
import resource 

time_start = time.perf_counter()
# insert code here ...
time_elapsed = (time.perf_counter() - time_start)
memMb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0/1024.0
print ("%5.1f secs %5.1f MByte" % (time_elapsed,memMb))
```

Remarque : il est nécessaire de faire un import supplémentaire : `import resource`

**—> Tableau des résultats obtenus :** (mémoire en MByte) testé avec `f = 5`

| Séquence / fichier test | méthode 1   | méthode 2 (classique) |
| ----------------------- | ----------- | --------------------- |
| cmv.fasta               | 26.6 MByte  | 28.8 MByte            |
| gfp.fasta               | 30.5 MByte  | 40.6 MByte            |
| calreticulin.fasta      | 194.0 MByte | 891.6 MByte           |

### Partie 2

La partie 2 se base sur la méthode inverse de la partie 1 méthode 1. 

- Si le fichier est compressé (`.idxc` et non `.idx`) : décompression puis ajout du `$` en fonction des informations de la première ligne. L’ouvberture n’étant pas la même pour un fichier binaire ou non, la vérification est faite par le nom du fichier et non le premier élément de la première ligne. 

- On recrée ensuite la matrice d’origine à partir de la séquence avec le `$`. 

- Les indexes sont retrouvés :
  - à partir de la len avant le `$` (étant incrémenté de 1 ligne par ligne comme les numéros de ligne)
  - des arrays enrengistrés dans les indexes du fichier d’où l’on part (renseigné tous les $f$ indexes)
    - Remarque : nous cherchons l’ordre des indexes pour pouvoir afficher les résultats dans l’ordre de la séquence du fichier `.idx(c)`. Ceci engendre aussi un re-parcours des indexes des deux listes à la fin du programme. 

### Partie 3

La partie 3 ne fut pas réalisée. Un début de piste fut débuté avec l’implémentation de la seconde version du 1 mais non terminé. 

La première méthode du 1 n’est pas suffisante pour rempalcer cette troisième partie, `zsh` kill le processus avant sa réalisation `rtn4.fasta`. 

