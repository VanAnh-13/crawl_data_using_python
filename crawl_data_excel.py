import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Headers to mimic a browser and avoid being blocked
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://balocenter.com/'
}

# List to store all data
all_data = []

# Base URL for the product listing
base_url = 'https://balocenter.com/collections/all'


# Function to crawl data from the product listing page
def crawl_listing_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        return False

    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.select('div.item.item-product.product-resize')

    if not products:
        print("No products found on this page.")
        return False

    for product in products:
        # Extract brand_name (vendor)
        brand_name_tag = product.find('div', class_='vendor')
        brand_name = brand_name_tag.text.strip() if brand_name_tag else 'Not available'

        # Extract name (title)
        name_tag = product.find('span', class_='title')
        name = name_tag.find('a').text.strip() if name_tag and name_tag.find('a') else 'Not available'

        # Extract price (sale price if available, otherwise original price)
        currency_sign = product.find('span', class_='currency-sign')
        price = ''
        if currency_sign:
            sale_price_tag = currency_sign.find('a')
            original_price_tag = currency_sign.find('del')
            price = sale_price_tag.text.strip() if sale_price_tag else (
                original_price_tag.text.strip() if original_price_tag else 'Not available')

        # Extract image_link
        image_tag = product.find('div', class_='image')
        image_link = image_tag.find('a').find('img')['src'] if image_tag and image_tag.find('a') and image_tag.find(
            'a').find('img') else 'Not available'

        # Extract detail_link
        detail_link_tag = product.find('span', class_='title')
        detail_link = detail_link_tag.find('a')['href'] if detail_link_tag and detail_link_tag.find(
            'a') else 'Not available'
        if detail_link and not detail_link.startswith('http'):
            detail_link = f"https://balocenter.com{detail_link}"

        # Create a dictionary for the product data
        product_data = {
            'brand_name': brand_name,
            'name': name,
            'price': price,
            'image_link': image_link,
            'detail_link': detail_link,
            'description': ''  # To be updated after crawling the detail page
        }

        # Crawl the detail page for additional data
        crawl_detail_page(detail_link, product_data)

        all_data.append(product_data)

    return True


# Function to crawl data from the product detail page
def crawl_detail_page(detail_url, product_data):
    try:
        response = requests.get(detail_url, headers=headers)
        if response.status_code != 200:
            print(f"Cannot access {detail_url}: {response.status_code}")
            product_data['description'] = 'Could not retrieve details'
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract product description
        description_row = soup.find('div', class_='row product-index detail-product description')
        if description_row:
            desc_divs = description_row.find_all('div', class_='desc')
            description_text = ''
            for div in desc_divs:
                # Extract text from all <p> tags
                paragraphs = div.find_all('p')
                for p in paragraphs:
                    description_text += p.text.strip() + ' '
                # Extract text from <ul> and <li> tags if present
                lists = div.find_all('ul')
                for ul in lists:
                    items = ul.find_all('li')
                    for li in items:
                        description_text += li.text.strip() + ' '
            product_data['description'] = description_text.strip()
        else:
            product_data['description'] = 'No description available'

    except Exception as e:
        print(f"Error crawling detail page {detail_url}: {e}")
        product_data['description'] = 'Error during crawling'


# Handle pagination
page = 1
while True:
    url = f"{base_url}?page={page}"
    print(f"Crawling page {page}: {url}")
    if not crawl_listing_page(url):
        break
    page += 1
    time.sleep(1)  # Delay to avoid being blocked

# Save data to an Excel file
if all_data:
    df = pd.DataFrame(all_data)
    columns = ['brand_name', 'name', 'price', 'image_link', 'detail_link', 'description']
    df.to_excel('products_with_details.xlsx', index=False, columns=columns)
    print(f"Saved {len(all_data)} products to products_with_details.xlsx")
else:
    print("No data to save.")