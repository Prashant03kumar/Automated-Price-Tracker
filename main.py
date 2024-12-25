# Automated price tracker
import requests
from bs4 import BeautifulSoup
import smtplib
import os

''' By using the headers, Amazon's server can respond with the right website for your region and your language.'''
'''Benefits: If you pass some headers along then Amazon's servers can give you the instant pot page in your language and also in your currency.'''

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Static URL
# url="https://appbrewery.github.io/instant_pot/"
# Live link of product you want to track

url = "https://www.amazon.com/dp/B075CYMYK6"

response = requests.get(url=url, headers=headers)

if response.status_code != 200:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
    exit()

# aok-offscreen

soup = BeautifulSoup(response.text, "html.parser")
price = soup.find('span', class_='a-offscreen')  # Updated the class to 'a-offscreen'

if not price:
    print("Price element not found. It could be due to Amazon's anti-scraping measures or incorrect class name.")
    exit()

# Safely extracting the price text
price_text = price.text.strip()
print(price_text)

# Find the span tag with the class 'productTitle'
title_tag = soup.find('span', class_='a-size-large product-title-word-break')

if not title_tag:
    print("Title element not found.")
    exit()

# Extract the numerical price without currency
try:
    price_without_currency = float(price_text.replace("$", "").replace(",", ""))  # Safely remove $ and commas
    print(price_without_currency)
except ValueError:
    print("Failed to parse the price value. Ensure the extracted text is a valid numerical value.")
    exit()

my_email = "pkritwan1020@gmail.com"
password = os.getenv("MY_PASSWORD")

BUY_PRICE = 100
if price_without_currency < BUY_PRICE:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(my_email, password)

        # Encode the message in UTF-8
        subject = "Price Alert!"
        body = f"{title_tag.text.strip()} is on sale for {price_without_currency}"

        '''We need to encode some non-ASCII characters'''
        msg = f"Subject: {subject}\n\n{body}".encode('utf-8')

        # Send the email
        connection.sendmail(
            from_addr=my_email,
            to_addrs="prashantserver2@gmail.com",
            msg=msg
        )
        print("Message has been sent!")
        connection.close()
else:
    print("No decline in Price")
