import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

names = pd.DataFrame({'car_name': ['Acura RL Sedan 2012', 'Audi A5 Coupe 2012', 'BMW 3 Series Sedan 2012', 'Cadillac SRX SUV 2012', 'Ford Ranger SuperCab 2011', 'Honda Accord Coupe 2012', 'Hyundai Tucson SUV 2012', 'MINI Cooper Roadster Convertible 2012', 'Toyota Camry Sedan 2012', 'Volvo C30 Hatchback 2012']})

# Function to remove the last word from a string
def remove_last_word(name):
    words = name.split()[:-1]  # Exclude the last word
    return ' '.join(words)

def scrape_car_data(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    car_data = {}

    try:
        car_data['price'] = soup.find('div', class_='price').find_next('span').get_text(strip=True)
        car_data['engine'] = soup.find('tr', class_='engine').find_next('td', class_='spec').get_text(strip=True)
        car_data['fuel'] = soup.find('tr', class_='mpg').find_next('td', class_='spec').get_text(strip=True)
        car_data['seating'] = soup.find('tr', class_='seating').find_next('td', class_='spec').get_text(strip=True)
        car_data['transmission'] = soup.find('tr', class_='transmission').find_next('td', class_='spec').get_text(strip=True)
        car_data['power'] = soup.find('tr', class_='power').find_next('td', class_='spec').get_text(strip=True)
    except AttributeError:
        print("Some elements might be missing.")
    
    return car_data

car_data = []

for model in names['car_name']:
    if model == 'BMW 3 Series Sedan 2012':
        url = 'https://www.autoblog.com/buy/2012-BMW-328/'
    elif model == 'MINI Cooper Roadster Convertible 2012':
        url = 'https://www.autoblog.com/buy/2012-MINI-Cooper-Base__2dr_Roadster/'
    else:
        # Extract year and model name for URL
        match = re.match(r"(.+?) (\d{4})$", model)
        if not match:
            print(f"Invalid format for car model: {model}")
            continue

        model_name, year = match.groups()
        # Apply the function to each entry in the 'car_name' column
        model_name = remove_last_word(model_name)
        model_name_encoded = re.sub(r'\s+', '-', model_name.strip())  # Replace spaces with hyphens and trim spaces
        url = f"https://www.autoblog.com/buy/{year}-{model_name_encoded}/"
    
    print(f"Scraping data for {model} from {url}...")
    data = scrape_car_data(url)
    
    if data:
        data['model_name'] = model
        car_data.append(data)
    
car_data_df = pd.DataFrame(car_data)
car_data_df.to_csv('car_data.csv', index=False)