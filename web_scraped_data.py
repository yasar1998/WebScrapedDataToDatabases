from bs4 import BeautifulSoup
import requests
import pymongo
import mysql.connector

## Specifying MongoDB details (NoSql Database)
# Local NoSql Database Server
myClient = pymongo.MongoClient('localhost')
# Database called "web_scraped_data" created or used if it exists
nosql_db = myClient['web_scraped_data']
# Collection called "watches_collection" created or used if it exists
collection = nosql_db['watches_collection']

## Specifying MySql Database details (Sql Database)
# Local Sql Database Server
sql_db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='web_scraped_data'   # After creating MySql database using terminal or code
)
myCursor = sql_db.cursor()
# myCursor.execute("CREATE Database web_scraped_data") -  Used to create database
# Table created
myCursor.execute("CREATE TABLE watches_table (name VARCHAR(255), price VARCHAR(255), shipping VARCHAR(255))")

# request the website of ebay (online shopping website)
html_text = requests.get("https://www.ebay.com/b/Wristwatches/31387/bn_2408451").text
# python library to read html content of website
soup = BeautifulSoup(html_text, 'lxml')
# collect 'li' tags with given class name into list
watches = soup.find_all('li', class_='s-item s-item--large s-item--bgcolored')

for watch in watches:
    # the textual content of
    # 'h3', 'span' tags with the specified class name scraped
    watch_name = watch.find('h3', class_='s-item__title').text
    price = watch.find('span', class_='s-item__price').text
    shipping = watch.find('span', class_='s-item__shipping s-item__logisticsCost').text
    # data is shown as a dictionary format (or json format)
    final_data = {'name': watch_name,
                  'price': price,
                  'shipping': shipping}
    # data is inserted into the noSql database
    collection.insert_one(final_data)

    # data is inserted into the Sql database
    myCursor.execute("INSERT INTO watches_table (name, price, shipping) VALUES (%s, %s, %s)",
                     (watch_name, price, shipping))
    sql_db.commit()
