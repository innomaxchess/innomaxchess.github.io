import requests 
from bs4 import BeautifulSoup
import json
from datetime import date

#
url = 'https://swissonlinetournament.com/Tournament/Rating/3f8e4252123e4b409c5fb1ae4f9aff83'

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.find('table')

    if table:

        json_data = []

        for row in table.find_all('tr')[1:]:
            row_data = {}

            columns = row.find_all(['td','th'])

            for idx, column in enumerate(columns):
                if idx == 1:
                    row_data['name'] = column.text.strip()
                elif idx == 2:
                    row_data['total'] = column.text.strip()
                else:
                    row_data[column.text.strip()] = column.text.strip()


            json_data.append(row_data)

        json_string = json.dumps(json_data, indent=2)

        today = date.today()
        file_path = 'month/'+today.strftime('%Y-%m-%d') + '.json'

        with open(file_path, 'w') as json_file:
            json.dump(json_string, json_file, indent=2)

        print(json_string)
        print(f"JSON data has been written to {file_path}")
    else:
        print("Table not found on the page")
else: 

    print("Failed to retrieve the page.")

