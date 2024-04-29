
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from io import StringIO

import time
import pandas as pd
import os

class Primeira:
    def __init__(self, url, directory, file_name_pattern):
        self.url = url
        self.directory = directory
        self.file_name_pattern = file_name_pattern
        self.driver = None

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)

    def scrape(self):
        self.setup_driver()
        self.driver.get(self.url)
        self.navigate_and_extract_categories()
        self.driver.quit()

    def navigate_and_extract_categories(self):
        categories = ['Summary', 'Offensive', 'Defensive', 'xG', 'Detailed']
        for category in categories:
            self.navigate_and_extract_category(category)

    def navigate_and_extract_xg_sub_tabs(self):
        # Primeiro, clique na aba xG para garantir que estamos começando do lugar certo
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "xG"))
        ).click()
        time.sleep(5)  # Aumente se necessário para garantir que a página carregou completamente

        # Vamos iterar sobre as sub-abas 'For' e 'Against'
        for value in ["true", "false"]:
            sub_tab_name = "Against" if value == "true" else "For"
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'a[data-value="{value}"][data-backbone-model-attribute="against"]'))
            ).click()
            time.sleep(2)  # Ajuste conforme necessário

            # Agora vamos iterar sobre 'Overall', 'Home' e 'Away' dentro de 'For' ou 'Against'
            for sub_sub_tab in ['Overall', 'Home', 'Away']:
                # Clique na sub-aba correspondente
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, sub_sub_tab))
                ).click()
                time.sleep(2)  # Ajuste conforme necessário

                # Chame a função de extração de dados para cada combinação de categoria e sub-aba
                self.navigate_pages_and_extract(f"xG_{sub_tab_name}", sub_sub_tab)

    def navigate_and_extract_detailed_sub_tabs(self):
        # Clique na aba "Detailed" antes de interagir com o dropdown
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Detailed"))
        ).click()
        time.sleep(5)  # Dê tempo para a página reagir à nova seleção

        select_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'category'))
        )
        select = Select(select_element)

        # Guarde as opções do dropdown para evitar StaleElementException
        options_values = [option.get_attribute('value') for option in select.options if option.get_attribute('value')]

        for option_value in options_values:
            print(f"Extraindo dados para a categoria Detailed: {option_value}")

            # Selecione a opção do dropdown
            select.select_by_value(option_value)
            time.sleep(2)  # Dê tempo para a página atualizar os dados da tabela

            # Agora itere sobre as sub-abas 'Overall', 'Home' e 'Away'
            for sub_tab in ['Overall', 'Home', 'Away']:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, sub_tab))
                ).click()
                time.sleep(2)  # Dê tempo para a página carregar

                # Extraia os dados para cada combinação de categoria e sub-aba
                self.navigate_pages_and_extract(f"Detailed_{option_value}", sub_tab)
    def navigate_and_extract_category(self, category_name):
        if category_name == "Summary":
            summary_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'stage-team-stats-summary'))
            )
            summary_element.click()
            time.sleep(5)
        else:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, category_name))
            ).click()
            time.sleep(5)

        if category_name == "xG":
            self.navigate_and_extract_xg_sub_tabs()
        elif category_name == "Detailed":
            self.navigate_and_extract_detailed_sub_tabs()
        else:
            for sub_tab in ['Overall', 'Home', 'Away']:
                self.navigate_and_extract_sub_tabs(category_name, sub_tab)

    def navigate_and_extract_sub_tabs(self, tab_category, sub_tab_name):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, sub_tab_name))).click()
            time.sleep(5)
            self.navigate_pages_and_extract(tab_category, sub_tab_name)
        except TimeoutException:
            print(f"Não foi possível encontrar a sub-aba '{sub_tab_name}' na categoria '{tab_category}'.")

    def navigate_pages_and_extract(self, tab_category, sub_tab_name):
        print(f"Last page for {tab_category} - {sub_tab_name} tab reached")
        self.extract_data_to_csv(tab_category, sub_tab_name)

    def extract_data_to_csv(self, tab_category, sub_tab_name):
        file_path = f"{self.directory}/{tab_category}_{sub_tab_name}_{self.file_name_pattern}.csv"
        file_exists = os.path.exists(file_path)
        header_elements = self.driver.find_elements(By.XPATH, "//*[@id='top-team-stats-summary-grid']//th")
        headers = [header.text for header in header_elements if header.text]
        elements = self.driver.find_elements(By.XPATH, "//*[@id='top-team-stats-summary-content']")
        for i in elements:
            p_db = i.get_attribute('innerHTML')
        p_db = '<table>' + p_db + '</table>'
        html_io = StringIO(p_db)
        df = pd.read_html(html_io)[0]
        if headers and len(df.columns) == len(headers):
            df.columns = headers
        header = not file_exists
        df.to_csv(file_path, mode='a', header=header, index=False)