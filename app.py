import warnings

import pandas as pd

warnings.filterwarnings('ignore')
import chromedriver_autoinstaller as ca
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def chrome_install(option=None, options=False):
    try:
        if options:
            driver = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
            driver.get("www.google.com")
            driver.close()
        else:
            driver = webdriver.Chrome(executable_path='chromedriver.exe')
            driver.get("www.google.com")
            driver.close()
    except:
        ca.install(cwd=True)
        driver = webdriver.Chrome(executable_path='chromedriver.exe')
        driver.close()
    return driver


def get_stocks(url):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('ignore-certificate-errors')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
    driver.get(url)
    stock = []
    try:
        table = driver.find_element(by='xpath',value='//*[@id="DataTables_Table_0"]')
        rows = table.find_element(by='xpath',value='//*[@id="DataTables_Table_0"]/tbody')
        rows = rows.find_elements(by='tag name',value='tr')
        for row in rows:
            cols = row.find_elements(by='tag name',value='td')
            if cols:
                stock.append([col.text for col in cols])
        return stock
    except BaseException as err:
        print(err.args)

if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('ignore-certificate-errors')
    driver = chrome_install(options=True, option=chrome_options)
    url = ''
    st = get_stocks(url)
    if len(st)>0:
        df =pd.DataFrame(st,columns=['Sr.no','Name','Symbol','Links','%CH','Price','Vol'])
        feature = ['Name','Symbol','%CH','Price']
        df = df[feature]
        print(df.head())