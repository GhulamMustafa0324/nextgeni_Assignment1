import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

olx_URL = 'https://www.olx.com.pk/item/iphone-15-pro-max-iphone-15-pro-max-256gb-non-pta-black-titanium-iid-1079699265'
surmawala_URL = 'https://surmawala.pk/apple-iphone-15-pro-max-256gb-natural-titanium-dual-sim'

# Scrape data
def data_scraping(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# Extract data
def data_extraction(soup, website_name):
    title = "Title Not Found"
    price = "Price Not Found"

    if website_name == 'OLX':
        title_tag = soup.find('h1', class_='a38b8112')
        if title_tag:
            title = title_tag.text.strip()

        price_tag = soup.find('span', class_='_56dab877')
        if price_tag:
            price = price_tag.text.strip()
    elif website_name == 'Surmawala':
        title_tag = soup.find('h1', class_='page-title')
        if title_tag:
            title = title_tag.find('span', class_='base').text.strip()

        price_tag = soup.find('span', class_='price')
        if price_tag:
            price = price_tag.text.strip()
    return {
        'site': website_name,
        'title': title,
        'price': price
    }

olx_data = data_scraping(olx_URL)
surmawala_data = data_scraping(surmawala_URL)

olx_product = data_extraction(olx_data, 'OLX')
surmawala_product = data_extraction(surmawala_data, 'Surmawala')

df = pd.DataFrame([olx_product, surmawala_product])

def clean_DF(df):
    # Remove any characters that are not a digit, a decimal point, or a comma
    df['price'] = df['price'].str.replace(r'[^\d.,]', '', regex=True)
    df['price'] = df['price'].str.replace(',', '')
    df['price'] = df['price'].str.lstrip('.')
    df['price'] = df['price'].replace('', np.nan)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

clean_DF(df)

# Compare prices
if not df.empty and 'price' in df.columns:
    cheaper_site = df.loc[df['price'].idxmin(), 'site']
    print(f"The cheaper option is available on {cheaper_site}.")
