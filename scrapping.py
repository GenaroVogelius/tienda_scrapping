from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os


# options = Options()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')  

# Crear una instancia del navegador Chrome con las opciones configuradas
# driver = webdriver.Chrome(options=options)

# URLS = ["https://www.elmundodelabijouterie.com.ar/etiqueta-producto/anillos-acero/", "https://www.elmundodelabijouterie.com.ar/etiqueta-producto/aros-acero/", ]
# self.driver.get("https://www.elmundodelabijouterie.com.ar/etiqueta-producto/por-paquetes/")


# vuelta = 0
# Define a function to check if new content has loaded
# def has_new_content_loaded(current_height):
#     # Scroll down to the bottom to trigger loading more content
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(5)  # Give it some time to load

#     # Get the new page height after scrolling
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     print("Cargando más info...")
    

#     # if vuelta == 10:
#     #     return False
#     # Check if new content has loaded (compare heights)
#     return new_height != current_height

# # Initialize variables
# scrolling = True
# page_height = driver.execute_script("return document.body.scrollHeight")

# # Scroll until no more new content is loaded
# while scrolling:
#     scrolling = has_new_content_loaded(page_height)
#     # vuelta += 1
#     page_height = driver.execute_script("return document.body.scrollHeight")


class Getter_info():
    def __init__(self):
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless') 
        self.driver = webdriver.Chrome(options=options)
        
        # self.driver.get(url)

        # self.scrolling = True
        # self.page_height = self.driver.execute_script("return document.body.scrollHeight")

        
        self.precios = []
        self.descripciones = []
        self.codigos = []

        # self.scroll()


    def get_html(self):
        self.page_source = self.driver.page_source
        self.soup = BeautifulSoup(self.page_source, 'lxml')

    def get_url(self, url):
        self.driver.get(url)

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

        # def scroller(self):
    
    def has_new_content_loaded(self, current_height):
    # Scroll down to the bottom to trigger loading more content
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Give it some time to load

        # Get the new page height after scrolling
        new_height = self.driver.execute_script("return document.body.scrollHeight")
        print("Cargando más info...")
    

        # if vuelta == 10:
        #     return False
        # Check if new content has loaded (compare heights)
        return new_height != current_height

# Scroll until no more new content is loaded
    def scroll(self):
        while self.scrolling:
            self.scrolling = self.has_new_content_loaded(self.page_height)
            self.page_height = self.driver.execute_script("return document.body.scrollHeight")
        self.get_html()
    

    def create_excel(self, urls, excel_files):
        for url, excel_file in zip(urls, excel_files):

            self.driver.get(url)
            self.scrolling = True
            self.page_height = self.driver.execute_script("return document.body.scrollHeight")
            self.scroll()

            self.precios.clear()
            self.descripciones.clear()
            self.codigos.clear()
            data = self.get_all_info_in_dict()


            # Create the DataFrame with the specified index
            df = pd.DataFrame(data)


            if os.path.exists(excel_file):
                # delete the excel file if exist
                os.remove(excel_file)

            # Write the DataFrame to an Excel file
            df.to_excel(excel_file, index=False)

            print(f"Excel '{excel_file}' creado exitosamente :)")




    #     is_bottom = False

    #     while not is_bottom:

    #         is_bottom = self.check_if_bottom()
    #         self.get_codigos_info()
    #         self.get_productos_info()
    #         self.get_price_info()



    #     while not is_bottom:
    #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         time.sleep(10)  # Give it some time to load

    #         # Get the new page height after scrolling
    #         new_height = driver.execute_script("return document.body.scrollHeight")
    #         print("Cargando más info...")

    #         if new_height != current_height:

    #         # Check if new content has loaded (compare heights)
    #             is_bottom = False
    #         page_height = driver.execute_script("return document.body.scrollHeight")
    #         return new_height != current_height

    # def check_if_bottom(self):
    #     current_height = driver.execute_script("return document.body.scrollHeight")

    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(10)  # Give it some time to load
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == current_height:
    #         return True
    #     else:
    #         return False


urls = ["https://www.elmundodelabijouterie.com.ar/etiqueta-producto/por-paquetes/", "https://www.elmundodelabijouterie.com.ar/etiqueta-producto/anillos-acero/", "https://www.elmundodelabijouterie.com.ar/etiqueta-producto/aros-acero/", "https://www.elmundodelabijouterie.com.ar/etiqueta-producto/cadenas-acero/", "https://www.elmundodelabijouterie.com.ar/etiqueta-producto/dijes-acero/", "https://www.elmundodelabijouterie.com.ar/etiqueta-producto/pulseras-acero/", "https://www.elmundodelabijouterie.com.ar/etiqueta-producto/acero-blanco/", "https://www.elmundodelabijouterie.com.ar/etiqueta-producto/acero-dorado/"]
excel_files = ["por_paquetes.xlsx","anillos.xlsx","aros.xlsx","cadenas.xlsx","dijes.xlsx","pulseras.xlsx","acero_blanco.xlsx","acero_dorado.xlsx"]

if len(urls) != len(excel_files):
    raise ValueError("The lengths of 'urls' and 'excel_files' are not equal.")

GI = Getter_info()

GI.create_excel(urls, excel_files)

# for url, excel_file in zip(urls, excel_files):
#     GI = Getter_info(urls, excel_files)

#     GI.create_excel()

    # data = GI.get_all_info_in_dict()

    # print(len(data["Codigos"]))
    # print(len(data["Precios"]))
    # print(len(data["Descripcion"]))


    # # Create the DataFrame with the specified index
    # df = pd.DataFrame(data)


    # if os.path.exists(excel_file):
    #     # delete the excel file if exist
    #     os.remove(excel_file)

    # # Write the DataFrame to an Excel file
    # df.to_excel(excel_file, index=False)

    # print(f"Excel '{excel_file}' creado exitosamente :)")

