from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')  

# Crear una instancia del navegador Chrome con las opciones configuradas
driver = webdriver.Chrome(options=options)


driver.get("https://www.elmundodelabijouterie.com.ar/categoria-producto/acero/")


vuelta = 0
# Define a function to check if new content has loaded
def has_new_content_loaded(current_height):
    # Scroll down to the bottom to trigger loading more content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)  # Give it some time to load

    # Get the new page height after scrolling
    new_height = driver.execute_script("return document.body.scrollHeight")
    print("Cargando más info...")

    # Check if new content has loaded (compare heights)
    return new_height != current_height

# Initialize variables
scrolling = True
page_height = driver.execute_script("return document.body.scrollHeight")

# Scroll until no more new content is loaded
while scrolling:
    scrolling = has_new_content_loaded(page_height)
    page_height = driver.execute_script("return document.body.scrollHeight")


class Getter_info():
    def __init__(self, page_source):
        self.soup = BeautifulSoup(page_source, 'lxml')
        self.precios = []
        self.descripciones = []
        self.codigos = []

    def get_price_info(self):
        prices = self.soup.find_all("span", class_="woocommerce-Price-amount amount")
        for price in prices:
            if price.find_parent("del") is None:
                text = price.get_text()
                self.precios.append(text)
    
    def get_productos_info(self):
        productos_a = self.soup.find_all('a', href=lambda href: href and '/producto' in href)
        for producto in productos_a:
            text = producto.get_text().strip()
            if text != "" and text != 'Select options':
                self.descripciones.append(text)

    def get_codigos_info(self):
        codigos_span = self.soup.find_all("span", class_="sku_wrapper")
        for codigo in codigos_span:
            text = codigo.get_text()
            self.codigos.append(text)

    def get_all_info_in_dict(self):
        self.get_codigos_info()
        self.get_productos_info()
        self.get_price_info()
        data = {'Codigos': self.codigos, 'Precios': self.precios, 'Descripcion': self.descripciones}
        return data


page_source = driver.page_source
GI = Getter_info(page_source)

data = GI.get_all_info_in_dict()

# print(len(data["Codigos"]))
# print(len(data["Precios"]))
# print(len(data["Descripcion"]))
# GI.get_codigos_info()
# GI.get_productos_info()
# GI.get_price_info()
# print(len(GI.codigos))
# print(len(GI.descripciones))
# print(len(GI.precios))
# print(GI.codigos)
# print(GI.descripciones)
# print(GI.precios)

# data = {'Codigos': GI.codigos, 'precios': GI.precios, 'Descripcion': GI.descripciones}



# Create the DataFrame with the specified index
df = pd.DataFrame(data)
# Specify the file path for the Excel file
excel_file = 'bijouterie.xlsx'


if os.path.exists(excel_file):
    os.remove(excel_file)


# Write the DataFrame to an Excel file
df.to_excel(excel_file, index=False)

print(f"Excel '{excel_file}' creado exitosamente :)")
