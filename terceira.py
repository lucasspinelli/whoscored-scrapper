
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
import os
from io import StringIO

class Terceira:
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
        categories = {
            "Attack Sides": ("#stage-touch-channels", "stage-touch-channels-filter-field"),
            "Shot Directions": ("#stage-attempt-directions", "stage-attempt-directions-filter-field"),
            "Shot Zones": ("#stage-attempt-zones", "stage-attempt-zones-filter-field"),
            "Action Zones": ("#stage-touch-zones", "stage-touch-zones-filter-field")
        }
        for category_name, (category_hash, filter_div_id) in categories.items():
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"ul#stage-pitch-stats-options a[href='{category_hash}']"))
                ).click()
                time.sleep(5)
                if category_name in ["Shot Directions", "Shot Zones"]:
                    self.navigate_and_extract_for_against(category_name)
                else:
                    self.navigate_and_extract_sub_tabs(category_name, filter_div_id)
            except TimeoutException:
                print(f"Não foi possível encontrar a categoria '{category_name}'.")

    def navigate_and_extract_for_against(self, category_name):
        for_against_tabs = {
            "For": "0",
            "Against": "1"
        }
        filter_div_id_for_against = "stage-attempt-directions-filter-against" if category_name == "Shot Directions" else "stage-attempt-zones-filter-against"
        for sub_tab_name, data_source in for_against_tabs.items():
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, f"div#{filter_div_id_for_against} a[data-source='{data_source}']"))
                ).click()
                time.sleep(2)
                filter_div_id = "stage-attempt-directions-filter-field" if category_name == "Shot Directions" else "stage-attempt-zones-filter-field"
                self.navigate_and_extract_sub_tabs(f"{category_name} - {sub_tab_name}", filter_div_id)
            except TimeoutException:
                print(f"Não foi possível encontrar a sub-aba '{sub_tab_name}' para '{category_name}'.")

    def navigate_and_extract_sub_tabs(self, tab_category, filter_div_id):
        sub_tabs = {
            "Overall": "1",
            "Home": "2",
            "Away": "3"
        }
        for sub_tab_name, data_value in sub_tabs.items():
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"div#{filter_div_id} a[data-value='{data_value}']"))
                ).click()
                time.sleep(2)
                self.extract_data_to_csv(tab_category, sub_tab_name)
            except TimeoutException:
                print(f"Não foi possível encontrar a sub-aba '{sub_tab_name}' na categoria '{tab_category}'.")

    def extract_data_to_csv(self, tab_category, sub_tab_name, additional_tab=''):
        file_path = f"{self.directory}/{tab_category}_{sub_tab_name}{additional_tab}_{self.file_name_pattern}.csv"
        file_exists = os.path.exists(file_path)
        file_empty = True if not file_exists or os.path.getsize(file_path) == 0 else False
        df = pd.DataFrame()  # Your extraction logic and saving to CSV will be handled here

        if tab_category == "Attack Sides":
            header_elements = self.driver.find_elements(By.XPATH, "//*[@id='stage-touch-channels-grid']//th")
            headers = [header.text for header in header_elements if header.text]

            elements = self.driver.find_elements(By.XPATH, """//*[@id="stage-touch-channels-content"]""")

            # Atualiza headers e df baseado na categoria selecionada
            headers = [header.text for header in header_elements if header.text]
            for i in elements:
                p_db = i.get_attribute('innerHTML')
            p_db = '<table>' + p_db + '</table>'
            html_io = StringIO(p_db)
            df = pd.read_html(html_io)[0]

            if headers and len(df.columns) == len(headers):
                df.columns = headers

        if tab_category == 'Shot Directions - For' or tab_category == 'Shot Directions - Against':
            header_elements = self.driver.find_elements(By.XPATH, "//*[@id='stage-attempt-directions-grid']//th")
            headers = [header.text for header in header_elements if header.text]

            elements = self.driver.find_elements(By.XPATH, """//*[@id="stage-attempt-directions-content"]""")

            # Atualiza headers e df baseado na categoria selecionada
            headers = [header.text for header in header_elements if header.text]
            for i in elements:
                p_db = i.get_attribute('innerHTML')
                print(p_db)

            p_db = '<table>' + p_db + '</table>'
            html_io = StringIO(p_db)
            df = pd.read_html(html_io)[0]

            if headers and len(df.columns) == len(headers):
                df.columns = headers

        if tab_category == "Shot Zones - For" or tab_category == "Shot Zones - Against":
            header_elements = self.driver.find_elements(By.XPATH, "//*[@id='stage-attempt-zones-grid']//th")
            headers = [header.text for header in header_elements if header.text]
            elements = self.driver.find_elements(By.XPATH, """//*[@id="stage-attempt-zones-content"]""")

            # Atualiza headers e df baseado na categoria selecionada
            headers = [header.text for header in header_elements if header.text]
            for i in elements:
                p_db = i.get_attribute('innerHTML')
            p_db = '<table>' + p_db + '</table>'
            html_io = StringIO(p_db)
            df = pd.read_html(html_io)[0]

            if headers and len(df.columns) == len(headers):
                df.columns = headers

        if tab_category == "Action Zones":
            header_elements = self.driver.find_elements(By.XPATH, "//*[@id='stage-touch-zones-grid']//th")
            headers = [header.text for header in header_elements if header.text]
            elements = self.driver.find_elements(By.XPATH, """//*[@id="stage-touch-zones-content"]""")

            # Atualiza headers e df baseado na categoria selecionada
            headers = [header.text for header in header_elements if header.text]
            for i in elements:
                p_db = i.get_attribute('innerHTML')
            p_db = '<table>' + p_db + '</table>'
            html_io = StringIO(p_db)
            df = pd.read_html(html_io)[0]

            if headers and len(df.columns) == len(headers):
                df.columns = headers

        # Utiliza 'file_empty' para determinar se o cabeçalho deve ser incluído
        df.to_csv(file_path, mode='a', header=file_empty, index=False)