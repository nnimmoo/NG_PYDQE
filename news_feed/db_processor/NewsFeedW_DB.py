import importlib.util
import os
import logging
from db_processor import DatabaseProcessor

module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'manual_inputer', 'manual_inputer.py')

spec = importlib.util.spec_from_file_location("manual_inputer", module_path)
manual_inputer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_inputer)

NewsFeed = manual_inputer.NewsFeed

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class NewsFeedWithDB(NewsFeed):
    def __init__(self, filename="News Feed.txt", db_processor=None):
        super().__init__(filename)
        self.db_processor = db_processor if db_processor else DatabaseProcessor()

    def addRecord(self, record):
        lines = record.strip().split('\n')

        if lines[0] == "--BREAKING NEWS--":
            text = lines[1]
            city = lines[2].split(',')[0]
            if self.db_processor.process_record('news', text=text, city=city):
                formatted_record = super().publishNews(text, city)
                super().addRecord(formatted_record)
        elif lines[0] == "--AD--":
            text = lines[1]
            expiration_date = lines[2].split(': ')[1].split(',')[0]
            if self.db_processor.process_record('ad', text=text, expiration_date=expiration_date):
                formatted_record = super().publishAd(text, expiration_date)
                super().addRecord(formatted_record)
        elif lines[0] == "--Weather Forecast--":
            city = lines[1].split(': ')[1]
            temperature = lines[2].split(': ')[1].rstrip('*C')
            conditions = lines[3].split(': ')[1]
            if self.db_processor.process_record('weather', city=city, temperature=temperature, conditions=conditions):
                formatted_record = super().publishWeather(city, temperature, conditions)
                print(formatted_record, 'here')
                super().addRecord(formatted_record)
        else:
            logging.warning(f"Unrecognized record format: {record}")

    def __del__(self):
        if self.db_processor:
            self.db_processor.close_connection()


if __name__ == "__main__":
    news_feed = NewsFeedWithDB()

    # Test
#     news_feed.addRecord("""--BREAKING NEWS--
# New park opened in the city center
# New York, 25/03/2026 10:30""")
#
#     # Test
#     news_feed.addRecord("""--AD--
# Summer sale at City Mall
# Expiration date: 30/08/2026, 157 days left""")
#
#     # Test
#     news_feed.addRecord("""--Weather Forecast--
# City: London
# Temperature: 22*C
# Weather: Partly cloudy""")
#
#
#     db_processor = news_feed.db_processor
#     db_processor.cursor.execute("SELECT * FROM news")
#     print("News records:", db_processor.cursor.fetchall())
#     db_processor.cursor.execute("SELECT * FROM ad")
#     print("Ad records:", db_processor.cursor.fetchall())
#     db_processor.cursor.execute("SELECT * FROM weather")
#     print("Weather records:", db_processor.cursor.fetchall())