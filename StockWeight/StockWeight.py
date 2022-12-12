from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By

nasdaq_loc="https://www.slickcharts.com/nasdaq100"
sp500_loc="https://www.slickcharts.com/sp500"

def getStocks(driver, location):
    driver.get(location)
    print(driver.title)
    table = driver.find_element(By.CLASS_NAME, 'table-responsive')
    elements = table.find_elements(By.TAG_NAME, 'tr')

    stocks = []
    for element in elements:
        rows = element.find_elements(By.TAG_NAME, 'td')
        if len(rows) > 4:
#        stock = rows[2].text
#        weight = rows[3].text
#        price = rows[4].text
            stocks.append( [rows[2].text, rows[3].text, rows[4].text])
#   print(*stocks, sep='\n' )
    return stocks

options = FirefoxOptions()
options.add_argument("--headless")

driver=webdriver.Firefox(options=options)
sp500 = getStocks(driver, sp500_loc)

nasdq_100 = getStocks(driver, nasdaq_loc)
print(*sp500, sep='\n' )
print(*nasdq_100, sep='\n' )

driver.close()
driver.quit()

