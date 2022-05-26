from bs4 import BeautifulSoup
import requests
import smtplib
import os
import lxml
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("MY_EMAIL")
RECEIVER_EMAIL = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("PASSWORD")
URL = "https://www.amazon.com/MSI-RTX-3080-LHR-10G/dp/B09FSWGS7L/ref=sr_1_3?crid=17VI5FNE16PQC&keywords=3080+graphics+card&qid=1653028159&sprefix=3080%2Caps%2C70&sr=8-3"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(URL, headers=headers)
page = response.text

soup = BeautifulSoup(page, "lxml")

price = float(soup.find(name="span", class_="a-offscreen").getText().replace("$", ""))
print(price)
name = (
    soup.find(
        name="span", id="productTitle", class_="a-size-large product-title-word-break"
    )
    .getText()
    .strip()
)
print(name)

if price <= 880:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(user=SENDER_EMAIL, password=PASSWORD)
        server.sendmail(
            from_addr=SENDER_EMAIL,
            to_addrs=RECEIVER_EMAIL,
            msg=f"Subject:PRICE DROP ALERT\n\n{name} is now {price}\n{URL}",
        )
        server.close()
