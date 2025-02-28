import json
import os
import datetime
from manual_inputer.manual_inputer import NewsFeed

class JSONProcessor:
    def __init__(self, news_feed, default_folder="json_input"):
        self.news_feed = news_feed
        self.default_folder = default_folder

    def process_json(self, file_path=None):
        if file_path is None:
            file_path = self.get_default_json_file()
        
        if file_path is None or not os.path.exists(file_path):
            print(f"JSON file not found: {file_path}")
            return

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            if isinstance(data, list):
                for record in data:
                    self.process_record(record)
            elif isinstance(data, dict):
                self.process_record(data)
            else:
                raise ValueError("Invalid JSON format. Expected a list of records or a single record.")

            # Remove the file after successful processing
            os.remove(file_path)
            print(f"File {file_path} processed and removed successfully.")

        except json.JSONDecodeError:
            print(f"Error: {file_path} is not a valid JSON file.")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

    def get_default_json_file(self):
        if not os.path.exists(self.default_folder):
            print(f"Default folder {self.default_folder} does not exist.")
            return None

        json_files = [f for f in os.listdir(self.default_folder) if f.endswith('.json')]
        if not json_files:
            print(f"No JSON files found in {self.default_folder}")
            return None

        return os.path.join(self.default_folder, json_files[0])

    def process_record(self, record):
        record_type = record.get('type', '').lower()
        if record_type == 'news':
            self.news_feed.addRecord(self.news_feed.publishNews(record.get('text'), record.get('city')))
        elif record_type == 'ad':
            self.news_feed.addRecord(self.news_feed.publishAd(record.get('text'), record.get('expiration_date')))
        elif record_type == 'weather':
            self.news_feed.addRecord(self.news_feed.publishWeather(record.get('city'), record.get('temperature'), record.get('conditions')))
        else:
            print(f"Unknown record type: {record_type}")

def main():
    news_feed = NewsFeed()
    json_processor = JSONProcessor(news_feed)

    while True:
        print("\nSelect an option:")
        print("1. Process JSON file from default folder")
        print("2. Process JSON file from custom path")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            json_processor.process_json()
        elif choice == '2':
            file_path = input("Enter the path to the JSON file: ").strip()
            json_processor.process_json(file_path)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()