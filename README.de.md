# SellerSprite-Marktforschung und BI

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Die ausdrücklich gewünschte Ausgabesprache verwenden, sonst der Sprache der Anfrage folgen. Befehle, Skill-IDs, JSON-Schlüssel, Enumerationswerte, Einheiten und Originalzitate unverändert lassen. Übersetzungen kennzeichnen. Land, Währung und Rechtsordnung nicht aus der Sprache ableiten. Relevante Detailreferenzen lesen und sämtliche bestehenden Prüfungen und Berechtigungsgrenzen einhalten.

## Installation und Nutzung

Das Repository herunterladen oder klonen und das angegebene Skill-Verzeichnis mit seinen vorhandenen references, scripts, assets und weiteren Abhängigkeiten in das Skill-Verzeichnis des Hosts kopieren. Name und SKILL.md beibehalten. Ein Sprachwechsel erfordert keine weitere Installation. Installationsbefehle sind Optionen und kein Nachweis einer Installation oder Aktivierung.

```sh
git clone https://github.com/PDBen-Auto/sellersprite-amazon-market-research-bi-skill.git
```

## SellerSprite-Marktforschung und BI

`sellersprite-bi-market-research`

Aus Startbegriffen relevante ASINs entdecken, Marktebenen trennen und Exporte parent-dedupliziert zu prüfbarem BI verarbeiten.

Skill-Verzeichnis: `.`

**Umsetzungsgrundlage und Abhängigkeiten**

Definierter Markt/Produktauftrag, Standard-/Detail-XLSX und benötigte Keyworddateien, Python 3/openpyxl. Online braucht autorisiertes SellerSprite-Konto/Browser. Schätzungen sind keine Amazon-Abrechnungsdaten.

**Eingaben**

Umfang/Datum/Marktplatz/Ein- und Ausschluss; seed_keyword/seed_asins für Entdeckung; bedingt Keyword-/Standard-/Detailexporte. Optional Relevanz, Attribute, Ziele. Keine Zugangsdaten.

**Ausgaben**

Kandidatenmanifest mit Gründen und Detailabdeckung; Parent-/Monats-/Jahres-/YTD-/Perioden-/Markenumsatz-/Rangmomentumdaten; eigenständiges dashboard.html, Prüfung und Lücken.

[Ablauf · Grenzen und Abbruchbedingungen · Beispielanfrage](references/i18n/de.md)

> Verwende `$sellersprite-bi-market-research` — Aus Keyword-/Wettbewerberexporten direktes Markt-BI erstellen und nicht abgedeckte Kandidaten aus dem Umsatznenner halten; antworte auf Deutsch und erhalte Belege, unbekannte Werte und Berechtigungsgrenzen.

## Sprachumfang und Prüfung

Dieser lokalisierte Leitfaden umfasst Zweck, Voraussetzungen, Ein- und Ausgaben, Ablauf, Beispiele und Grenzen. Er übersetzt nicht jede Referenz Zeile für Zeile. Technische Detailreferenzen, historische Fälle, Skriptfehler, Beispieloberflächen und Bilder bleiben in der Originalsprache und können auf Wunsch erläutert werden. Struktur, Links und Kernbedingungen werden geprüft; ein muttersprachliches Lektorat je Sprache wird nicht behauptet.

Vor der Übergabe Eingaben, Belege, fehlende Werte, Ausgabedateien und ursprüngliche Abschlusskriterien abgleichen. Nicht ausgeführte Schritte als ungeprüft kennzeichnen; ein erfolgreicher Skriptablauf bestätigt keine geschäftliche Aussage.
