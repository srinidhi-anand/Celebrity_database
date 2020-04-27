# Import Python Libraries for the url access and database
import os
import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import DatabaseError
import xlsxwriter


def create_db_connection(db_filepath): # Function to Create a database connection to access the local file directory
    conn = None
    try:
        conn = sqlite3.connect(db_filepath)
    except (Exception, DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            return conn


def create_table(conn): # Function to Create a table to write the data in the table
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS CELEB_DATA (SNo INTEGER PRIMARY KEY autoincrement, Name TEXT, Img TEXT, url TEXT);""")
    conn.commit()


page = requests.get('https://www.imdb.com/list/ls068010962/') # url of celebrity images and their information
soup = BeautifulSoup(page.text, 'html.parser')

# Variable declarations
List_data = []
row = 0
col = 0

# Links to be decomposed to avoid data tidiness
links = soup.find(class_='text-muted text-small')
links.decompose()

artist_name_list = soup.find(class_='lister-list')
artist_images = artist_name_list.find_all('img')
artist_content = artist_name_list.find_all('p')

# Initiating the Excel sheet to write the information
workbook = xlsxwriter.Workbook('Celebrity Database.xlsx')
worksheet = workbook.add_worksheet()

# Adding the column names in the Excel File
worksheet.write(row, col, 'Names')
worksheet.write(row, col + 1, 'Images Links')
worksheet.write(row, col + 2, 'Personality traits')

# Data is looped to get as list as well import it in Excel
for images, desc in zip(artist_images, artist_content):
    List_data.append({'Names': images.get('alt'), 'Images': images.get('src'), 'Links': desc.contents[0]})
    worksheet.write(row, col, images.get('alt'))
    worksheet.write(row, col + 1, images.get('src'))
    worksheet.write(row, col + 2, desc.contents[0])

workbook.close() # close the worksheet as data is written

db_filepath = os.path.dirname('Celebrity Database.xlsx') # Created Excel File is connected with the SQL database
conn = create_db_connection(db_filepath) # Function call to open connection and create table
create_table(conn)
for data in List_data:
    c = conn.cursor()
    # Insert Data into the table once the table is created
    c.execute("""INSERT INTO CELEB_DATA (Name, Img, url) VALUES (?,?,?);""",(data['Names'], data['Images'],data['Links']))
    conn.commit()
