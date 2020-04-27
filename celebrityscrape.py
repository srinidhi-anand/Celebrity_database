import os
import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import DatabaseError
import xlsxwriter


def create_db_connection(db_filepath):
    conn = None
    try:
        conn = sqlite3.connect(db_filepath)
    except (Exception, DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            return conn


def create_table(conn):
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS CELEB_DATA (SNo INTEGER PRIMARY KEY autoincrement, Name TEXT, Img TEXT, url TEXT);""")
    conn.commit()


page = requests.get('https://www.imdb.com/list/ls068010962/')
soup = BeautifulSoup(page.text, 'html.parser')
List_data = []
row = 0
col = 0

links = soup.find(class_='text-muted text-small')
links.decompose()

artist_name_list = soup.find(class_='lister-list')
artist_images = artist_name_list.find_all('img')
artist_content = artist_name_list.find_all('p')

workbook = xlsxwriter.Workbook('Celebrity Database.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(row, col, 'Names')
worksheet.write(row, col + 1, 'Images Links')
worksheet.write(row, col + 2, 'Personality traits')

for images, desc in zip(artist_images, artist_content):
    List_data.append({'Names': images.get('alt'), 'Images': images.get('src'), 'Links': desc.contents[0]})
    worksheet.write(row, col, images.get('alt'))
    worksheet.write(row, col + 1, images.get('src'))
    worksheet.write(row, col + 2, desc.contents[0])

workbook.close()

db_filepath = os.path.dirname('Celebrity Database.xlsx')
conn = create_db_connection(db_filepath)
create_table(conn)
for data in List_data:
    c = conn.cursor()
    c.execute("""INSERT INTO CELEB_DATA (Name, Img, url) VALUES (?,?,?);""",(data['Names'], data['Images'],data['Links']))
    conn.commit()
