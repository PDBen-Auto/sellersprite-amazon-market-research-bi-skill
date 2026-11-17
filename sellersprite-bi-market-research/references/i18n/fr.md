# Recherche marché SellerSprite et BI

`sellersprite-bi-market-research` · Français

## Objectif et périmètre

Étendre l’intention initiale aux ASIN pertinents, séparer les couches et dédupliquer par parent pour un BI auditable.

## Fondements et dépendances

Marché/tâche définis, XLSX standard/détaillé et mots-clés nécessaires, Python 3/openpyxl. Collecte en ligne : compte/navigateur SellerSprite autorisés. Estimations ≠ règlements Amazon.

## Entrées

Périmètre/date/marché/inclusion-exclusion, seed_keyword/seed_asins pour découverte ; exports mots-clés/standard/détaillé conditionnels ; pertinence/attributs/destinations facultatifs. Aucun identifiant secret.

## Sorties

Manifest candidats motivés/couverture détaillée ; données parent/mois/année/YTD/périodes/chiffre d’affaires marque/momentum ; dashboard.html autonome, audit et lacunes.

## Déroulement

1. Fixer tâche
2. regrouper mots-clés et core_direct/adjacent_substitute/excluded_noise/review
3. examiner indécis/exclusions importantes
4. dénominateur limité aux produits acceptés couverts
5. dédupliquer parent/mois sans addition des variantes
6. séparer unités/CA/GMV modélisé/mois comparables
7. rangs globaux fixes, momentum distinct des opportunités
8. rapprocher chiffres et tester filtres/images/pages.

## Limites et conditions d’arrêt

Échantillon de recherche ≠ TAM catégorie. Sans détail, pas d’historique ; sans CA, marque/rang N/A. Inconnu ≠0. Séparer US/CA/MX. Aucun contournement ; rang d’échantillon par CA, pas Amazon BSR.

## Exemple de demande

Utilise `$sellersprite-bi-market-research` — Créer le BI du marché direct depuis mots-clés/concurrents sans ajouter les candidats non couverts au dénominateur des ventes ; réponds en français en conservant les preuves, les inconnues et les limites d’autorisation.

## Spécification complète

[Point d’entrée du Skill et références détaillées](../../SKILL.md).

Utiliser la langue explicitement demandée, sinon celle de la demande. Conserver les commandes, identifiants de Skill, clés JSON, valeurs d’énumération, unités et citations originales. Distinguer traduction et original. Ne déduire ni pays, ni devise, ni juridiction de la langue. Lire les références détaillées utiles et maintenir tous les contrôles et autorisations existants.

Avant livraison, rapprocher entrées, preuves, valeurs manquantes, fichiers et critères d’achèvement d’origine. Marquer les étapes non exécutées comme non vérifiées ; la réussite d’un script ne valide pas une conclusion métier.

## Couverture linguistique et validation

Ce guide localisé couvre objectif, prérequis, entrées, sorties, étapes, exemples et limites. Il ne traduit pas chaque référence ligne par ligne. Les références techniques détaillées, cas historiques, erreurs de scripts, interfaces d’exemple et images restent dans leur langue originale et peuvent être expliqués à la demande. Structure, liens et contraintes essentielles sont vérifiés ; aucune relecture par un locuteur natif de chaque langue n’est revendiquée.

