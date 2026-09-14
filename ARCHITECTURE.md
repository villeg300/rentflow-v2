# RentFlow — Architecture

## 1. Architecture générale

RentFlow utilise une architecture séparant clairement le frontend et le backend.

```text
┌─────────────────────┐
│      FRONTEND       │
│      Next.js        │
└──────────┬──────────┘
           │
           │ HTTP / REST API
           │
┌──────────▼──────────┐
│       BACKEND       │
│ Django + DRF        │
└──────────┬──────────┘
           │
           │
┌──────────▼──────────┐
│     PostgreSQL      │
└─────────────────────┘
```

## 2. Backend

Le backend sera développé avec :

* Python ;
* Django ;
* Django REST Framework ;
* PostgreSQL.

Le backend sera responsable de :

* l'authentification ;
* la logique métier ;
* la validation des données ;
* les permissions ;
* l'accès à la base de données ;
* l'API REST.

## 3. Frontend

Le frontend sera développé avec :

* Next.js ;
* TypeScript ;
* Tailwind CSS.

Le frontend sera responsable de :

* l'interface utilisateur ;
* la navigation ;
* les formulaires ;
* l'affichage des données ;
* la communication avec l'API.

## 4. Organisation du backend

L'organisation interne du backend sera définie progressivement en fonction des domaines métier.

Les principales applications envisagées sont :

```text
authentication
properties
tenants
leases
payments
maintenance
```

Aucune application ne sera créée avant qu'un besoin métier justifie son existence.

## 5. Organisation du frontend

Le frontend sera organisé autour des fonctionnalités du produit.

Les composants génériques seront séparés des composants spécifiques aux fonctionnalités.

L'architecture ne doit pas introduire d'abstraction avant qu'elle soit nécessaire.

## 6. Communication

Le frontend communique avec le backend exclusivement à travers l'API REST.

```text
Next.js
   │
   │ HTTP
   ▼
Django REST Framework
   │
   ▼
PostgreSQL
```

## 7. Principes d'architecture

### Simplicité

Privilégier la solution la plus simple qui répond correctement au besoin.

### Séparation des responsabilités

Chaque couche doit avoir une responsabilité clairement définie.

### Compréhensibilité

Le code doit pouvoir être compris par le développeur du projet sans dépendre d'une génération automatique.

### Évolution progressive

L'architecture doit évoluer avec les besoins réels du produit.

### Pas de sur-ingénierie

Aucune abstraction, technologie ou infrastructure ne doit être ajoutée uniquement parce qu'elle est disponible ou populaire.
