# SellerSprite-Marktforschung und BI

`sellersprite-bi-market-research` · Deutsch

## Zweck und Einsatzbereich

Aus Startbegriffen relevante ASINs entdecken, Marktebenen trennen und Exporte parent-dedupliziert zu prüfbarem BI verarbeiten.

## Umsetzungsgrundlage und Abhängigkeiten

Definierter Markt/Produktauftrag, Standard-/Detail-XLSX und benötigte Keyworddateien, Python 3/openpyxl. Online braucht autorisiertes SellerSprite-Konto/Browser. Schätzungen sind keine Amazon-Abrechnungsdaten.

## Eingaben

Umfang/Datum/Marktplatz/Ein- und Ausschluss; seed_keyword/seed_asins für Entdeckung; bedingt Keyword-/Standard-/Detailexporte. Optional Relevanz, Attribute, Ziele. Keine Zugangsdaten.

## Ausgaben

Kandidatenmanifest mit Gründen und Detailabdeckung; Parent-/Monats-/Jahres-/YTD-/Perioden-/Markenumsatz-/Rangmomentumdaten; eigenständiges dashboard.html, Prüfung und Lücken.

## Ablauf

1. Auftrag einfrieren
2. Keywords clustern und core_direct/adjacent_substitute/excluded_noise/review zuweisen
3. offene und große Ausschlüsse prüfen
4. nur akzeptierte detailliert abgedeckte Produkte in den Nenner
5. Parent/Monat deduplizieren, Geschwister nicht addieren
6. Einheiten/Umsatz/Modell-GMV/Monatsmengen trennen
7. globale Stichprobenränge fixieren, Momentum und Chance trennen
8. Zahlen, Filter, Bilder und Seiten prüfen.

## Grenzen und Abbruchbedingungen

Suchstichprobe ist kein Kategorie-TAM. Ohne Detail keine Historienaussage; ohne Umsatz Markenumsatz/Rang N/A. Unbekannt ist nicht0. US/CA/MX getrennt. Kein Zugangs-Bypass; Rang ist Stichprobenumsatz, nicht Amazon BSR.

## Beispielanfrage

Verwende `$sellersprite-bi-market-research` — Aus Keyword-/Wettbewerberexporten direktes Markt-BI erstellen und nicht abgedeckte Kandidaten aus dem Umsatznenner halten; antworte auf Deutsch und erhalte Belege, unbekannte Werte und Berechtigungsgrenzen.

## Vollständige Spezifikation

[Skill-Einstieg und Detailreferenzen](../../SKILL.md).

Die ausdrücklich gewünschte Ausgabesprache verwenden, sonst der Sprache der Anfrage folgen. Befehle, Skill-IDs, JSON-Schlüssel, Enumerationswerte, Einheiten und Originalzitate unverändert lassen. Übersetzungen kennzeichnen. Land, Währung und Rechtsordnung nicht aus der Sprache ableiten. Relevante Detailreferenzen lesen und sämtliche bestehenden Prüfungen und Berechtigungsgrenzen einhalten.

Vor der Übergabe Eingaben, Belege, fehlende Werte, Ausgabedateien und ursprüngliche Abschlusskriterien abgleichen. Nicht ausgeführte Schritte als ungeprüft kennzeichnen; ein erfolgreicher Skriptablauf bestätigt keine geschäftliche Aussage.

## Sprachumfang und Prüfung

Dieser lokalisierte Leitfaden umfasst Zweck, Voraussetzungen, Ein- und Ausgaben, Ablauf, Beispiele und Grenzen. Er übersetzt nicht jede Referenz Zeile für Zeile. Technische Detailreferenzen, historische Fälle, Skriptfehler, Beispieloberflächen und Bilder bleiben in der Originalsprache und können auf Wunsch erläutert werden. Struktur, Links und Kernbedingungen werden geprüft; ein muttersprachliches Lektorat je Sprache wird nicht behauptet.

