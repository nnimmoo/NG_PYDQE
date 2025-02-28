import datetime
import sys
import os

# Get the path to the NG_PYDQE directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the NG_PYDQE directory to the Python path
sys.path.append(parent_dir)

from functions.task3 import capitalizeSentences
from manual_inputer.manual_inputer import NewsFeed
from csvp.main import CSVProcessor

class TXTFileProcessor:
    def __init__(self, news_feed, input_folder="input_files", output_folder="output"):
        self.news_feed = news_feed
        self.input_folder = input_folder
        self.output_folder = os.path.join(parent_dir, output_folder)
        
        # Ensure the output folder exists
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def process_file(self):
        num_records = self.get_num_records()
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

        output_file = os.path.join(self.output_folder, "News Feed.txt")
        
        for record in records[:num_records]:
            normalized_record = self.normalize_text(record['content'])
            if record['type'] == 'news':
                self.add_to_output_file(output_file, self.news_feed.publishNews(normalized_record, record['city']))
            elif record['type'] == 'ad':
                self.add_to_output_file(output_file, self.news_feed.publishAd(normalized_record, record['expiration_date']))
            elif record['type'] == 'weather':
                self.add_to_output_file(output_file, self.news_feed.publishWeather(record['city'], record['temperature'], normalized_record))

        print(f"Processed {min(num_records, len(records))} records from {file_path}")

    def get_num_records(self):
        while True:
            try:
                num_records = int(input("How many records do you want to parse? "))
                if num_records > 0:
                    return num_records
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")

    def get_file_path(self):
        default_file = self.get_default_file()
        if default_file:
            use_default = input(f"Use default file ({default_file})? (y/n): ").lower().strip()
            if use_default == 'y':
                return os.path.join(self.input_folder, default_file)
        
        while True:
            file_path = input("Enter the path to the text file: ").strip()
            if os.path.exists(file_path):
                return file_path
            else:
                print(f"File not found: {file_path}")
                retry = input("Do you want to try again? (y/n): ").lower().strip()
                if retry != 'y':
                    return None

    def get_default_file(self):
        files = [f for f in os.listdir(self.input_folder) if f.endswith('.txt')]
        return files[0] if files else None

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

    def add_to_output_file(self, file_path, content):
        with open(file_path, 'a') as file:
            file.write(content)

if __name__ == "__main__":
    news_feed = NewsFeed()
    file_processor = TXTFileProcessor(news_feed)

    while True:
        print("\nSelect an option:")
        print("1. Manual input")
        print("2. Process file")
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

    csv_processor = CSVProcessor()
    csv_processor.process()