# RentFlow Frontend — Backlog

Ce fichier contient uniquement les tâches liées au frontend de RentFlow.

Le frontend doit rester simple, cohérent et directement aligné sur `PRODUCT.md`.

---

# 1. Fondations

## Initialisation

* [ ] Initialiser Next.js
* [ ] Configurer TypeScript
* [ ] Configurer Tailwind CSS
* [ ] Configurer ESLint
* [ ] Définir la structure des dossiers
* [ ] Configurer les variables d'environnement
* [ ] Configurer la communication avec l'API backend

## Interface générale

* [ ] Créer le layout principal
* [ ] Créer la navigation principale
* [ ] Créer le header
* [ ] Créer le système de notifications UI
* [ ] Créer les états de chargement
* [ ] Créer les états d'erreur
* [ ] Créer les pages 404 et erreurs

---

# 2. Authentification

* [ ] Page de connexion
* [ ] Formulaire de connexion
* [ ] Gestion du token
* [ ] Déconnexion
* [ ] Protection des routes privées
* [ ] Gestion des rôles
* [ ] Page de profil

---

# 3. Dashboard

Le dashboard doit présenter uniquement les informations utiles à la gestion quotidienne.

* [ ] Créer le dashboard
* [ ] Afficher les logements occupés
* [ ] Afficher les logements disponibles
* [ ] Afficher les loyers à encaisser
* [ ] Afficher les paiements en retard
* [ ] Ajouter les actions rapides nécessaires

---

# 4. Biens

## Liste

* [ ] Page de liste des biens
* [ ] Afficher les informations essentielles
* [ ] État vide
* [ ] Chargement
* [ ] Gestion des erreurs

## Création

* [ ] Formulaire de création
* [ ] Validation
* [ ] Envoi vers l'API

## Modification

* [ ] Formulaire de modification
* [ ] Validation
* [ ] Envoi vers l'API

## Détails

* [ ] Page de détail d'un bien
* [ ] Afficher ses logements
* [ ] Actions disponibles

---

# 5. Logements

## Liste

* [ ] Liste des logements
* [ ] Afficher le statut du logement
* [ ] Afficher le locataire actuel si nécessaire
* [ ] État vide

## Création

* [ ] Formulaire de création
* [ ] Validation
* [ ] Envoi vers l'API

## Modification

* [ ] Modification d'un logement
* [ ] Modification du statut

## Détails

* [ ] Page de détail
* [ ] Informations essentielles
* [ ] Locataire actuel
* [ ] Contrat actuel

---

# 6. Locataires

## Liste

* [ ] Liste des locataires
* [ ] Recherche simple
* [ ] Afficher les informations essentielles

## Création

* [ ] Formulaire de création
* [ ] Validation

## Modification

* [ ] Modifier les informations
* [ ] Validation

## Détails

* [ ] Page de détail
* [ ] Informations personnelles
* [ ] Logement actuel
* [ ] Contrat actuel
* [ ] Historique des paiements

---

# 7. Contrats

## Liste

* [ ] Liste des contrats
* [ ] Afficher le statut
* [ ] Afficher le locataire
* [ ] Afficher le logement

## Création

* [ ] Sélectionner le logement
* [ ] Sélectionner le locataire
* [ ] Définir le loyer
* [ ] Définir le dépôt de garantie
* [ ] Définir la date de début
* [ ] Définir la date de fin
* [ ] Validation

## Détails

* [ ] Page de détail
* [ ] Informations du contrat
* [ ] Informations financières
* [ ] Historique des paiements

## Résiliation

* [ ] Action de résiliation
* [ ] Confirmation
* [ ] Mise à jour de l'état

---

# 8. Paiements

## Liste

* [ ] Liste des paiements
* [ ] Afficher le montant
* [ ] Afficher le locataire
* [ ] Afficher le contrat
* [ ] Afficher la date utile du paiement

## Création

* [ ] Formulaire d'enregistrement
* [ ] Sélection du locataire
* [ ] Sélection du contrat
* [ ] Montant
* [ ] Date du paiement
* [ ] Validation

## Détails

* [ ] Page de détail d'un paiement

---

# 9. Maintenance

## Liste

* [ ] Liste des demandes
* [ ] Afficher le statut
* [ ] Afficher le logement
* [ ] Afficher la priorité si nécessaire

## Création

* [ ] Formulaire de demande
* [ ] Description
* [ ] Logement concerné
* [ ] Validation

## Suivi

* [ ] Modifier le statut
* [ ] Consulter les détails
* [ ] Clôturer une demande

---

# 10. UX et qualité

Ces tâches seront réalisées progressivement et uniquement l
