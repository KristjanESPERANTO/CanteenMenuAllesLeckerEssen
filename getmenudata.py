import pandas # To handle DataFrames
import camelot.io as camelot # To get tables out of an PDF file
import json
from datetime import date

# Setting the path for the output file
output_file = "./data/speiseplan.json"

# Getting the date variables to create the proper query URLs
current_date = date.today()
current_date_month = '{:02d}'.format(current_date.month)

first_url_year = str(current_date.year)
first_url_month = '{:02d}'.format(current_date.month - 1)
next_url_year = str(current_date.year)
next_url_month = '{:02d}'.format(current_date.month + 1)

# # Adapt the variables if it's January or December
if current_date.month == 1:
  first_url_year = str(current_date.year - 1)
  first_url_month = '12'
elif current_date.month == 12:
  next_url_year = str(current_date.year + 1)
  next_url_month = '01'

# Put the URLs together
source_file_this_month = "https://www.alles-lecker-essen.de/wp-content/uploads/" + first_url_year + "/" + first_url_month + "/Neutral" + current_date_month + first_url_year[-2:] + ".pdf"
source_file_this_month_withsmall_n = source_file_this_month.replace('Neutral', 'neutral')
source_file_next_month = "https://www.alles-lecker-essen.de/wp-content/uploads/" + next_url_year + "/" + current_date_month + "/Neutral" + next_url_month + next_url_year[-2:] + ".pdf"
source_file_next_month_withsmall_n = source_file_next_month.replace('Neutral', 'neutral')

# Put the URLs in an array
urls = [
  source_file_this_month,
  source_file_this_month_withsmall_n,
  source_file_next_month,
  source_file_next_month_withsmall_n,
]

# URL arrays for testing
# urls = ["https://www.alles-lecker-essen.de/wp-content/uploads/2021/10/Neutral1121.pdf",
#         "https://www.alles-lecker-essen.de/wp-content/uploads/2021/11/neutral1221.pdf"]
# urls = ["neutral1221.pdf"]


# Try to open all URLs and collect all tables
table_dataframes = []
print("Try to find the PDF files of the current and the next month.")
for url in urls:
  print(" Try to read file: " + url)
  try: 
      # Get all tabels in the PDF file - each page has one table
      tables = camelot.read_pdf(url, pages='all')
      print("  Found PDF file")
      # Put all table dataframes in one array
      for table in tables:
        table_dataframes.append(table.df)
  except: 
      print("  No readable PDF file found")

# Put all rows from all tables in one table
try:
  one_table = pandas.concat(table_dataframes, ignore_index=True)
except:
  print("No tables found.")
else:

  # Define table headers
  one_table.columns = ['date', 'menu1', 'menu2', 'menu3']

  # Clean up data
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

  # Go through every row/day - Create for every day an array - Put the menus as a dict in that array - Collect the day arrays in a dict
  data_dict = {}
  for idx, row in cleaned_table.iterrows():
      day_list = []
      i = 0
      for menu in row:
        if menu != "":
          i = i + 1
          menu_object = {}
          menu_object["_id"] = i
          menu_object["description"] = menu
          day_list.append(menu_object)
      data_dict[idx] = day_list

  # Dump the dict with the day arrays in a JSON string
  jsonString = json.dumps(data_dict, indent=2, ensure_ascii=False)

  if len(jsonString) > 100:
    # Write the result to JSON file
    jsonFile = open(output_file, "w")
    jsonFile.write(jsonString)
    jsonFile.close()
  else:
    print("Something seems to be wrong with the data. The file was not overwritten / written.")


  ## Output result
  print("\n\nThat's the collected data:")
  print(cleaned_table)
  print("You will find the data in this file: " + output_file + "\n")