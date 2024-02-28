"""
detailページへはボタンで遷移する
"""

import time
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def get_phone_text(input_text):
    """ 電話番号を抽出する関数 """
    pattern = r'\+\d{8,}'
    # 正規表現に一致するかどうかを判定
    match = re.search(pattern, input_text)
    if match:
        matched_text = match.group()
    else:
        matched_text = ""
    return matched_text




class KeywordScraper:
    def __init__(self , browse_visually = "no"):
        self.driver = self.browser_setup(browse_visually)
        self.wait_driver = WebDriverWait(self.driver, 10)
    
    def debug_page_html(self , file_name = "1"):
        html = self.wait_driver.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body"))).get_attribute("outerHTML")
        with open(file_name + ".html", "w", encoding="utf-8") as file:
            file.write(html)

    def browser_setup(self , browse_visually = "no" , user_agent_flag = False):
        """ブラウザを起動する関数"""
        options = webdriver.ChromeOptions()
        if browse_visually == "no":
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ') #追加
        driver = webdriver.Chrome(options=options , service=ChromeService(ChromeDriverManager().install()))
        driver.implicitly_wait(1)
        return driver
    
    def scraping(self , url , main_keyword):
        """ スクレイピングを実行する関数 """
        self.driver.get(url)
        # 検索窓にキーワードを入力
        search_box = self.driver.find_element(By.CSS_SELECTOR, '#keyword')
        search_box.send_keys(main_keyword)
        search_box.send_keys(Keys.ENTER)
        # 利用規約の確認ボタン
        time.sleep(2)
        site_rule_button = self.driver.find_element(By.CSS_SELECTOR, 'body > div.ui.dimmer.modals.page.transition.visible.active > div > div.actions > button.ui.green.ok.button')
        site_rule_button.click()
        time.sleep(5)
        soup = BeautifulSoup( self.driver.page_source , 'html.parser')
        suggest_keyword_list = soup.select(f'div > div.ui.active.tab.segment > div.ui.bottom.active.tab.segment > analyzed-by-keyword-rank > table > tbody > tr > td:nth-child(1)')
        search_vol_list = soup.select(f'#s_04 > div > div.ui.active.tab.segment > div.ui.bottom.active.tab.segment > analyzed-by-keyword-rank > table > tbody > tr > td:nth-child(2)')
        all_data = []
        for loop in range(len(suggest_keyword_list)):
            suggest_keyword = suggest_keyword_list[loop].text
            search_vol = search_vol_list[loop].text
            cleaned_search_vol = int( re.sub(r'[^0-9]', '', search_vol) )
            data = {
                'suggest keyword':suggest_keyword,
                'search vol':cleaned_search_vol,
            }
            all_data.append(data) 
        sorted_all_data = sorted(all_data, key=lambda x: x['search vol'], reverse=True)
        self.driver.quit()
        return sorted_all_data

