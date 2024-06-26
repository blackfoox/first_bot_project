import psycopg2
from bs4 import BeautifulSoup
import requests
import time
import random
import schedule

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                        password="yashka000", port="5432")

cur = conn.cursor()

#Создание sql
cur.execute("""CREATE TABLE IF NOT EXISTS person (
            game_name TEXT,
            game_link TEXT
);
""")

#Удаление всех данных из sql
with conn.cursor() as cursor:
    delet_query = "DELETE FROM person"
    cursor.execute(delet_query)

def parsing():
    #Итерация для заполучения игр с сайта
    page = 0
    while True:
        page += 1    
        url = 'https://stopgame.ru/games/new?p=' + str(page)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')

        data = soup.select("._card_1ovwy_1")
        time.sleep(1 + (random.random() * (9 - 5)))

        #Проверка на наличие определенной игры в sql 
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM person WHERE game_name = %s", (data[0]['title'], ))
            game = cursor.fetchone()

        #Добавление игр в sql и проверка с условием на наличие дубликата. Если данная игра есть в списке, условие не сработает и мы выходим из цикла.
        if not game:
            for item in data:
                cur.execute("""INSERT INTO person (game_name, game_link)
                VALUES (%s, %s);
                """, (item["title"], f"https://stopgame.ru{item["href"]}"))
        else:
            break

print("hi")
print('asdwasd')

def main():
    schedule.every().monday.at('10:00').do(parsing)

    while True:
        schedule.run_pending()

if __name__ == '_main_':
    main()

print('He2')

conn.commit()
cur.close()
conn.close()