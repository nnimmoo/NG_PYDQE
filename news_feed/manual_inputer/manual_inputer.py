import datetime
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from csvp.main import CSVProcessor
from db_processor.db_processor import DatabaseProcessor


class NewsFeed:
    def __init__(self, filename="News Feed.txt", db_processor=None):
        self.filename = filename
        self.output_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        self.db_processor = db_processor if db_processor else DatabaseProcessor()

    def getUserInput(self, prompt):
        return input(prompt).strip()

    def publishNews(self, text=None, city=None):
        if text is None:
            text = self.getUserInput("Enter news text: ")
        if city is None:
            city = self.getUserInput("Enter city: ")
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        return f"-- BREAKING NEWS --\n{text}\n{city}, {date}\n\n"

    def publishAd(self, text=None, expiration_date=None):
        if text is None:
            text = self.getUserInput("Enter ad text: ")

        while True:
            if expiration_date is None:
                expiration_date = self.getUserInput("Enter expiration date (DD/MM/YYYY): ")
            try:
                exp_date = datetime.datetime.strptime(expiration_date, "%d/%m/%Y")
                days_left = (exp_date - datetime.datetime.now()).days
                if days_left < 0:
                    print("The expiration date cannot be in the past. Please enter a future date.")
                    expiration_date = None
                    continue
                break
            except ValueError:
                print("Invalid date format. Please use DD/MM/YYYY.")
                expiration_date = None

        return f"-- AD --\n{text}\nExpiration date: {expiration_date}, {days_left} days left\n\n"

    def publishWeather(self, city=None, temperature=None, conditions=None):
        if city is None:
            city = self.getUserInput("Enter city: ")
        if temperature is None:
            temperature = self.getUserInput("Enter temperature (in Celsius): ")
        if conditions is None:
            conditions = self.getUserInput("Enter weather conditions: ")
        return f"-- Weather Forecast -- \nCity: {city}\nTemperature: {temperature}*C\nWeather: {conditions}\n\n"

    def addRecord(self, record):
        lines = record.strip().split('\n')

        if lines[0] == "-- BREAKING NEWS --":
            text = lines[1]
            city = lines[2].split(',')[0]
            if self.db_processor.process_record('news', text=text, city=city):
                self._writeToFile(record)
                print("News record added successfully!")
            else:
                print("Duplicate news record. Not added.")
        elif lines[0] == "-- AD --":
            text = lines[1]
            expiration_date = lines[2].split(': ')[1].split(',')[0]
            if self.db_processor.process_record('ad', text=text, expiration_date=expiration_date):
                self._writeToFile(record)
                print("Ad record added successfully!")
            else:
                print("Duplicate ad record. Not added.")
        elif lines[0] == "-- Weather Forecast --":
            city = lines[1].split(': ')[1]
            temperature = lines[2].split(': ')[1].rstrip('*C')
            conditions = lines[3].split(': ')[1]
            if self.db_processor.process_record('weather', city=city, temperature=temperature, conditions=conditions):
                self._writeToFile(record)
                print("Weather record added successfully!")
            else:
                print("Duplicate weather record. Not added.")
        else:
            print(f"Unrecognized record format: {record}")
            return

        csv_processor = CSVProcessor()
        csv_processor.process()

    def _writeToFile(self, record):
        output_file = os.path.join(self.output_folder, self.filename)
        with open(output_file, "a") as file:
            file.write(record)

    def run(self):
        while True:
            print("\nSelect record type to add:")
            print("1. News")
            print("2. Private Ad")
            print("3. Weather Forecast")
            print("4. Exit")

            choice = self.getUserInput("Enter your choice (1-4): ")

            if choice == '1':
                record = self.publishNews()
            elif choice == '2':
                record = self.publishAd()
            elif choice == '3':
                record = self.publishWeather()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")
                continue

            self.addRecord(record)

    def __del__(self):
        if self.db_processor:
            self.db_processor.close_connection()


# Output is in news_feed/output folder (due to newer tasks having one common file)
if __name__ == "__main__":
    news_feed = NewsFeed()
    news_feed.run()