import pandas # To handle DataFrames
import camelot.io as camelot # To get tables out of an PDF file
import json

source_file_this_month = "https://www.alles-lecker-essen.de/wp-content/uploads/2021/10/Neutral1121.pdf"
source_file_next_month = "https://www.alles-lecker-essen.de/wp-content/uploads/2021/11/neutral1221.pdf"
source_file_test = "neutral1221.pdf"

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
## Clear cells with the value 0 in it
cleaned_table = cleaned_table.replace(['0'], '')

## Set date as index
cleaned_table = cleaned_table.set_index('date')

data_dict = {}

for idx, row in cleaned_table.iterrows():
    day_list = []
    print(idx, row[0], row[1])
    i = 0
    for menu in row:
      if menu != "":
        i = i + 1
        menu_object = {}
        menu_object["Menü" + str(i)] = menu
        day_list.append(menu_object)
    data_dict[idx] = day_list
    
jsonString = json.dumps(data_dict, sort_keys=True, indent=2, ensure_ascii=False)

# Write result to JSON file
jsonFile = open("speiseplan.json", "w")
jsonFile.write(jsonString)
jsonFile.close()

## Output result
print(cleaned_table)
