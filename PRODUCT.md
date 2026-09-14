# RentFlow — Product Definition

## 1. Vision

RentFlow est un outil de gestion locative simple permettant à un propriétaire ou à un gestionnaire immobilier de centraliser la gestion de ses biens, logements, locataires, contrats et paiements.

## 2. Utilisateurs

### Propriétaire

Le propriétaire peut :

* gérer ses biens ;
* gérer les logements associés ;
* enregistrer ses locataires ;
* créer et gérer les contrats ;
* suivre les loyers ;
* enregistrer les paiements ;
* identifier les retards ;
* suivre les problèmes de maintenance.

### Gestionnaire

Le gestionnaire peut gérer les biens qui lui sont confiés et effectuer les opérations autorisées par le propriétaire.

### Locataire

Le locataire peut :

* consulter les informations de son logement ;
* consulter son contrat ;
* consulter ses paiements ;
* connaître son prochain loyer ;
* signaler un problème de maintenance.

## 3. Fonctionnalités principales

### Biens

Un bien représente une propriété immobilière contenant un ou plusieurs logements.

Exemples :

* immeuble ;
* maison ;
* résidence.

### Logements

Un logement appartient à un bien.

Exemples :

* appartement A01 ;
* appartement A02 ;
* studio B01.

Un logement peut être :

* disponible ;
* occupé ;
* en maintenance.

### Locataires

Un locataire représente une personne occupant un logement dans le cadre d'un contrat.

### Contrats

Un contrat relie :

```text
Locataire
    ↓
Logement
```

avec notamment :

* loyer mensuel ;
* dépôt de garantie ;
* date de début ;
* date de fin ;
* statut du contrat.

### Paiements

RentFlow doit permettre d'enregistrer les paiements effectués par les locataires et de suivre les montants dus.

### Maintenance

Un locataire ou un gestionnaire peut signaler un problème concernant un logement.

Le problème doit pouvoir être suivi jusqu'à sa résolution.

## 4. Principes produit

RentFlow doit respecter les principes suivants :

### Simplicité

Chaque fonctionnalité doit être compréhensible sans formation technique.

### Utilité

Une fonctionnalité ne doit être ajoutée que si elle répond à un besoin réel.

### Rapidité

Les opérations courantes doivent nécessiter le moins d'actions possible.

### Clarté

L'interface ne doit afficher que les informations utiles à la prise de décision.

### Progressivité

Les fonctionn
