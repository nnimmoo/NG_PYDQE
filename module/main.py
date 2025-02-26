import datetime
import sys
import os

# Get the path to the NG_PYDQE directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the NG_PYDQE directory to the Python path
sys.path.append(parent_dir)

# Now you can import from functions
from functions.task3 import capitalizeSentences
from classes.main import NewsFeed


class FileProcessor:
    def __init__(self, news_feed, default_folder="input_files"):
        self.news_feed = news_feed
        self.default_folder = default_folder

    def process_file(self, file_path=None):
        if file_path is None:
            file_path = self.get_file_path()
        
        if file_path is None:
            print("\nNo file to process.")
            return

        if not os.path.exists(file_path):
            print(f"\nFile not found: {file_path}")
            return

        with open(file_path, 'r') as file:
            content = file.read()

        records = self.parse_records(content)

        for record in records:
            normalized_record = self.normalize_text(record['content'])
            if record['type'] == 'news':
                self.news_feed.addRecord(self.news_feed.publishNews(normalized_record, record['city']))
            elif record['type'] == 'ad':
                self.news_feed.addRecord(self.news_feed.publishAd(normalized_record, record['expiration_date']))
            elif record['type'] == 'weather':
                self.news_feed.addRecord(self.news_feed.publishWeather(record['city'], record['temperature'], normalized_record))

        os.remove(file_path)
        print(f"File {file_path} processed and removed successfully.")

    def get_file_path(self):
        files = [f for f in os.listdir(self.default_folder) if f.endswith('.txt')]
        if not files:
            print(f"No text files found in {self.default_folder}")
            return None
        return os.path.join(self.default_folder, files[0])

    def parse_records(self, content):
        records = []
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            if lines[i].startswith('NEWS:'):
                news_text = lines[i+1]
                city = lines[i+2]
                records.append({'type': 'news', 'content': news_text, 'city': city})
                i += 3
            elif lines[i].startswith('AD:'):
                ad_text = lines[i+1]
                expiration_date = lines[i+2]
                records.append({'type': 'ad', 'content': ad_text, 'expiration_date': expiration_date})
                i += 3
            elif lines[i].startswith('WEATHER:'):
                city = lines[i+1]
                temperature = lines[i+2]
                conditions = lines[i+3]
                records.append({'type': 'weather', 'city': city, 'temperature': temperature, 'content': conditions})
                i += 4
            else:
                i += 1
        return records

    def normalize_text(self, text):
        return capitalizeSentences(text.lower())

if __name__ == "__main__":
    news_feed = NewsFeed()
    file_processor = FileProcessor(news_feed)

    while True:
        print("\nSelect an option:")
        print("1. Manual input")
        print("2. Process file, located in input_files folder")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            news_feed.run()
        elif choice == '2':
            file_processor.process_file()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")