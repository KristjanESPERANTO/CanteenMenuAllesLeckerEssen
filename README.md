# SpeiseplanAllesLeckerEssen

With the script `getmenudata.py`, the canteen menus for the current and the following month are read out from PDF files from a [caterer in Halle, Germany](https://www.alles-lecker-essen.de) and converted into a JSON file.

This is a special use case and will hardly be of interest to anyone.

## TODO
- cron-Job erstellen, der die Daten regelmäßig holt
- Falls vom aktuellen Monat keine Daten vorhanden: Alte Daten nicht überschreiben
- Installationsanleitung für Python-Skript hier im Repo erstellen
- unsere Installationsanleitung ergänzen
- öffentliches GitHub-Projekt erstellen
  - cron-Job erstellen, der aktuellen Daten vom GitHub-Projekt holt: git pull + Daten in .gitignore aufnehmen

## DONE
- Prüfen ob PDF-Files vom aktuellen und kommenden Monat vorhanden
- Falls beide vorhanden: beide zusammenführen
- MagicMirror-Modul bauen
