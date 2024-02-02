import requests
from bs4 import BeautifulSoup
import time

telegram_bot_token = '6669597585:AAG8edEOc_0fhWdYYAUrCxPWy8IEfq0JvOQ'
telegram_channel_username = '@deliveraddisbooks'

url = 'https://deliveraddis.com/books/eb-amharic-books'

def fetch_content(url):
    response = requests.get(url)
    return response.text
    
# Function to scrape book data from the HTML code
def scrape_data(html_code):
    soup = BeautifulSoup(html_code, "html.parser")
    books = []
    items = soup.find_all("div", class_="column product-column")
    for item in items:
        # Extracting Image URL
        image_tag = item.find("img", class_="lazyload")
        image_url = image_tag["data-src"] if image_tag else "Image URL not found"
        # Extracting Book Name
        name_tag = item.find("div", class_="product-name")
        name = name_tag.text.strip() if name_tag else "Name not found"
        # Extracting Author
        details = item.find_all("span", class_="properties")
        author = details[0].text.strip() if len(details) > 0 else "Author not found"
          # Extracting Category
        category = details[1].text.strip() if len(details) > 1 else "Category not found"
        # Extracting Price
        price_tag = item.find("p", class_="price")
        price = price_tag.text.strip() if price_tag else "Price not found"
        books.append({
            "Image URL": image_url,
            "Name": name,
            "Author": author,
            "Category": category,
            "Price": price
        })
    return books
    
#Function to send a message to a Telegram channel
def send_message_to_telegram(message):
    send_message_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {
        "chat_id": telegram_channel_username,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(send_message_url, data=data)
    if response.status_code != 200:
        print("Failed to send message to Telegram channel.")
        
# function that arranges the scraping and messaging process
def main():
    html_code = fetch_content(url)
    books_data = scrape_data(html_code)
    for book in books_data:
        caption = f"<b>Name:</b> {book['Name']}\n"
        caption += f"<b>Author:</b> {book['Author']}\n"
        caption += f"<b>Category:</b> {book['Category']}\n"
        caption += f"<b>Price:</b> {book['Price']}\n"
        caption += f"<b>Image URL:</b> {book['Image URL']}"
        send_message_to_telegram(caption)
        time.sleep(8)

if __name__ == "__main__":
    main()  # Calling the main function if the script is executed directly
