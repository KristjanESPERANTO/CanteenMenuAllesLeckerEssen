'''
TODO:
- Prüfen ob PDF-Files vom aktuellen und kommenden Monat vorhanden
- Falls beide vorhanden: beide zusammenführen
- Falls vom aktuellen Monat nicht vorhanden: Alte Daten nehmen und Hinweis erstellen
- Allergene und Zutaten im Modul auflisten (JSON dafür manuell erstellen)
- MagicMirror-Modul bauen
- cron-Job erstellen, der die Daten regelmäßig holt
- GitHub-Projekt erstellen
- cron-Job erstellen, der aktuellen Daten vom GitHub-Projekt holt
- Installationsanleitung für Python-Skript erstellen
'''

import pandas # To handle DataFrames
import camelot.io as camelot # To get tables out of an PDF file

source_file_this_month = "https://www.alles-lecker-essen.de/wp-content/uploads/2021/09/Neutral1021.pdf"
source_file_next_month = "https://www.alles-lecker-essen.de/wp-content/uploads/2021/10/Neutral1121.pdf"
source_file_test = "Neutral1121.pdf"

# Get all tabels in the PDF file - each page has one table
tables_this_month = camelot.read_pdf(source_file_this_month, pages='all')
tables_next_month = camelot.read_pdf(source_file_next_month, pages='all')

# Put all table dataframes in one array
table_dataframes = []
for table in tables_this_month:
  table_dataframes.append(table.df)

for table in tables_next_month:
  table_dataframes.append(table.df)

# Put all rows from all tables in one table
one_table = pandas.concat(table_dataframes, ignore_index=True)

# Define Table headers
one_table.columns = ['date', 'menu1', 'menu2', 'menu3']

# Clean up Data
## Remove line breaks
cleaned_table = one_table.replace('\n',' ', regex=True)
## Remove multible spaces
cleaned_table = cleaned_table.replace(' {2,}',' ', regex=True)
## Remove dublicates
cleaned_table = cleaned_table.drop_duplicates()
## Remove rubbish rows
cleaned_table = cleaned_table[cleaned_table.menu1 != "A"]
cleaned_table = cleaned_table[cleaned_table.menu1 != "0"]

## Set date as index
cleaned_table = cleaned_table.set_index('date')

## Output result
print(cleaned_table)

# Write result to JSON file
cleaned_table.to_json('speiseplan.json', force_ascii=False, orient='index', indent=2 )