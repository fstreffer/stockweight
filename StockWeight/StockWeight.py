from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from datetime import date
import locale
import sqlalchemy as db
from sqlalchemy.sql.sqltypes import Integer, Date, String, Float
from sqlalchemy.sql.functions import func

nasdaq_loc="https://www.slickcharts.com/nasdaq100"
sp500_loc="https://www.slickcharts.com/sp500"
db_location="sqlite://stocktest.db"

def getStocks(driver, location):
    driver.get(location)
    print(driver.title)
    table = driver.find_element(By.CLASS_NAME, 'table-responsive')
    elements = table.find_elements(By.TAG_NAME, 'tr')
    today = date.today()
    stocks = []
    for element in elements:
        rows = element.find_elements(By.TAG_NAME, 'td')
        if len(rows) > 4:
            stocks.append( { 'date' : today, 'index' : location, 'ticker' : rows[2].text, 'weight' : locale.atof(rows[3].text), 'price' : locale.atof(rows[4].text) })
    return stocks

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

options = FirefoxOptions()
options.headless = True

driver=webdriver.Firefox(options=options)

sp500 = getStocks(driver, sp500_loc)
nasdq_100 = getStocks(driver, nasdaq_loc)

print(*sp500, sep='\n' )
print(*nasdq_100, sep='\n' )

driver.close()
driver.quit()

#eopen database
engine = db.create_engine('sqlite:///stockstest.db')
connection = engine.connect()
metadata = db.MetaData()
#check Table
try: 
    stockweight_table = db.Table('stockweight', metadata, autoload=True, autoload_with=engine)
    print('table stockweight exists')
except db.exc.NoSuchTableError:
    #create Table it it does not exist
    print('creating table stockweight')
    stockweight_table = db.Table('stockweight', metadata, 
    db.Column('id', Integer, primary_key = True),
    db.Column('date', Date),
    db.Column('index', String),
    db.Column('ticker', String),
    db.Column('weight', Float),
    db.Column('price', Float))
    metadata.create_all(engine)
    
print(stockweight_table)

#does data already exist in db for today
s = db.select([func.count()]).select_from(stockweight_table).where(stockweight_table.c.date == date.today())
db_result = connection.execute(s)
result = db_result.fetchone()
print(f'found {result[0]}')
if (result[0]==0):
    #insert data
    connection.execute(stockweight_table.insert(), sp500)
    connection.execute(stockweight_table.insert(), nasdq_100)
    
    print('something')
else:
    print(f'db contains data for today {date.today()}')
#close db

