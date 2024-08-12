import psycopg2
from bs4 import BeautifulSoup
import requests
import time
import random

class GameScraper:
    def __init__(self, db_config):
        """"Инициализация соединения с базой данных"""
        self.conn = psycopg2.connect(**db_config)
        self.cur = self.conn.cursor()

    def create_table(self):
        """"Создание таблицы, если она отсутствует"""
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS person (
                game_name TEXT,
                game_link TEXT
            );
        """)

    def clear_table(self):
        """"Удаление всех данных из таблицы."""
        self.cur.execute("DELETE FROM person")
        self.conn.commit()

    def parse_games(self):
        """"Парсинг сайта и добавление новых игр в базу данных"""
        page = 0
        while True:
            page += 1
            url = f'https://stopgame.ru/games/new?p={page}'
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            data = soup.select("._card_1u499_4")
            time.sleep(1 + (random.random() * (9 - 5)))

            #Проверка на наличие определенной игры в SQL
            if data:
                self.cur.execute("SELECT * FROM person WHERE game_name = %s", (data[0]['title'],))
                game = self.cur.fetchone()
                
                if not game:
                    for item in data:
                        self.cur.execute("""
                            INSERT INTO person (game_name, game_link)
                            VALUES (%s, %s);
                        """, (item["title"], f"https://stopgame.ru{item['href']}"))
                        self.conn.commit()
                    else:
                        break
                    
                
    def close_connection(self):
        """"Закрытие соединения с базой данных"""
        self.cur.close()
        self.conn.close()

# Использование класса


db_config = {
    'host': "localhost",
    'dbname': "postgres",
    'user': "postgres",
    'password': "yashka000",
    'port': "5432"
}

scraper = GameScraper(db_config)
scraper.create_table()
scraper.clear_table()
scraper.parse_games()
scraper.close_connection()