import sqlite3
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class DatabaseProcessor:
    def __init__(self, db_name="news_feed.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.initialize_database()

    def initialize_database(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Create tables if they don't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                city TEXT NOT NULL,
                date TEXT NOT NULL,
                UNIQUE(text, city, date)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ad (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                expiration_date TEXT NOT NULL,
                UNIQUE(text, expiration_date)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY,
                city TEXT NOT NULL,
                temperature TEXT NOT NULL,
                conditions TEXT NOT NULL,
                date TEXT NOT NULL,
                UNIQUE(city, temperature, conditions, date)
            )
        ''')

        self.conn.commit()
        logging.debug("Database initialized")

    def add_news(self, text, city):
        date = datetime.now().strftime("%d/%m/%Y %H:%M")
        try:
            # duplicate check
            self.cursor.execute('''
                SELECT * FROM news WHERE text = ? AND city = ?
            ''', (text, city))
            if self.cursor.fetchone():
                logging.warning(f"Duplicate news entry not added: {text}, {city}")
                return False

            self.cursor.execute('''
                INSERT INTO news (text, city, date)
                VALUES (?, ?, ?)
            ''', (text, city, date))
            self.conn.commit()
            logging.debug(f"News added: {text}, {city}, {date}")
            return True
        except sqlite3.IntegrityError:
            logging.warning(f"Duplicate news entry not added: {text}, {city}, {date}")
            return False

    def add_ad(self, text, expiration_date):
        try:
       # duplicate check
            self.cursor.execute('''
                SELECT * FROM ad WHERE text = ? AND expiration_date = ?
            ''', (text, expiration_date))
            if self.cursor.fetchone():
                logging.warning(f"Duplicate ad entry not added: {text}, {expiration_date}")
                return False

            self.cursor.execute('''
                INSERT INTO ad (text, expiration_date)
                VALUES (?, ?)
            ''', (text, expiration_date))
            self.conn.commit()
            logging.debug(f"Ad added: {text}, {expiration_date}")
            return True
        except sqlite3.IntegrityError:
            logging.warning(f"Duplicate ad entry not added: {text}, {expiration_date}")
            return False

    def add_weather(self, city, temperature, conditions):
        date = datetime.now().strftime("%d/%m/%Y %H:%M")
        try:
            # duplicate check
            self.cursor.execute('''
                SELECT * FROM weather WHERE city = ? AND temperature = ? AND conditions = ?
            ''', (city, temperature, conditions))
            if self.cursor.fetchone():
                logging.warning(f"Duplicate weather entry not added: {city}, {temperature}, {conditions}")
                return False

            self.cursor.execute('''
                INSERT INTO weather (city, temperature, conditions, date)
                VALUES (?, ?, ?, ?)
            ''', (city, temperature, conditions, date))
            self.conn.commit()
            logging.debug(f"Weather added: {city}, {temperature}, {conditions}, {date}")
            return True
        except sqlite3.IntegrityError:
            logging.warning(f"Duplicate weather entry not added: {city}, {temperature}, {conditions}, {date}")
            return False

    def process_record(self, record_type, **kwargs):
        logging.debug(f"Processing record: type={record_type}, data={kwargs}")
        if record_type == 'news':
            return self.add_news(kwargs['text'], kwargs['city'])
        elif record_type == 'ad':
            return self.add_ad(kwargs['text'], kwargs['expiration_date'])
        elif record_type == 'weather':
            return self.add_weather(kwargs['city'], kwargs['temperature'], kwargs['conditions'])
        else:
            logging.error(f"Unknown record type: {record_type}")
            return False

    def close_connection(self):
        if self.conn:
            self.conn.close()
            logging.debug("Database connection closed")