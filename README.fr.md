# Recherche marché SellerSprite et BI

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Utiliser la langue explicitement demandée, sinon celle de la demande. Conserver les commandes, identifiants de Skill, clés JSON, valeurs d’énumération, unités et citations originales. Distinguer traduction et original. Ne déduire ni pays, ni devise, ni juridiction de la langue. Lire les références détaillées utiles et maintenir tous les contrôles et autorisations existants.

## Installation et utilisation

Télécharger ou cloner le dépôt, puis copier le répertoire du Skill indiqué, avec ses references, scripts, assets et autres dépendances existantes, dans le répertoire de Skills de l’hôte. Conserver son nom et SKILL.md. Changer la langue de documentation ne demande pas de nouvelle installation. Les commandes proposées ne prouvent ni installation ni activation.

```sh
git clone https://github.com/PDBen-Auto/sellersprite-amazon-market-research-bi-skill.git
```

## Recherche marché SellerSprite et BI

`sellersprite-bi-market-research`

Étendre l’intention initiale aux ASIN pertinents, séparer les couches et dédupliquer par parent pour un BI auditable.

Répertoire du Skill: `.`

**Fondements et dépendances**

Marché/tâche définis, XLSX standard/détaillé et mots-clés nécessaires, Python 3/openpyxl. Collecte en ligne : compte/navigateur SellerSprite autorisés. Estimations ≠ règlements Amazon.

**Entrées**

Périmètre/date/marché/inclusion-exclusion, seed_keyword/seed_asins pour découverte ; exports mots-clés/standard/détaillé conditionnels ; pertinence/attributs/destinations facultatifs. Aucun identifiant secret.

**Sorties**

Manifest candidats motivés/couverture détaillée ; données parent/mois/année/YTD/périodes/chiffre d’affaires marque/momentum ; dashboard.html autonome, audit et lacunes.

[Déroulement · Limites et conditions d’arrêt · Exemple de demande](references/i18n/fr.md)

> Utilise `$sellersprite-bi-market-research` — Créer le BI du marché direct depuis mots-clés/concurrents sans ajouter les candidats non couverts au dénominateur des ventes ; réponds en français en conservant les preuves, les inconnues et les limites d’autorisation.

## Couverture linguistique et validation

Ce guide localisé couvre objectif, prérequis, entrées, sorties, étapes, exemples et limites. Il ne traduit pas chaque référence ligne par ligne. Les références techniques détaillées, cas historiques, erreurs de scripts, interfaces d’exemple et images restent dans leur langue originale et peuvent être expliqués à la demande. Structure, liens et contraintes essentielles sont vérifiés ; aucune relecture par un locuteur natif de chaque langue n’est revendiquée.

Avant livraison, rapprocher entrées, preuves, valeurs manquantes, fichiers et critères d’achèvement d’origine. Marquer les étapes non exécutées comme non vérifiées ; la réussite d’un script ne valide pas une conclusion métier.
