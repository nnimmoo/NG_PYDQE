import datetime
import sys
import os

# Get the path to the project root directory (two levels up from the current file)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add the project root directory to the Python path
sys.path.append(project_root)

# Now you can import from functions
from functions.task3 import capitalizeSentences
from manual_inputer.manual_inputer import NewsFeed
from csvp.main import CSVProcessor

class TXTFileProcessor:
    def __init__(self, news_feed, input_folder=None, output_folder="output"):
        self.news_feed = news_feed
        if input_folder is None:
            self.input_folder = os.path.join(project_root, "news_feed", "txt_processor", "input_files")
        else:
            self.input_folder = os.path.join(project_root, input_folder)
        self.output_folder = os.path.join(project_root, output_folder)
        
        # Ensure the input and output folders exist
        os.makedirs(self.input_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)

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
        
        processed_records = 0
        for record in records:
            if processed_records >= num_records:
                break
            normalized_record = self.normalize_text(record['content'])
            if record['type'] == 'news':
                self.news_feed.addRecord(self.news_feed.publishNews(normalized_record, record['city']))
            elif record['type'] == 'ad':
                self.news_feed.addRecord(self.news_feed.publishAd(normalized_record, record['expiration_date']))
            elif record['type'] == 'weather':
                self.news_feed.addRecord(self.news_feed.publishWeather(record['city'], record['temperature'], normalized_record))
            processed_records += 1

        print(f"\nProcessed and added {processed_records} records from {file_path}")
        
        # os.remove(file_path)
        # print(f"File {file_path} has been removed after successful processing.")
        
    def get_num_records(self):
        while True:
            try:
                num_records = int(input("How many records from TXT file do you want to parse? "))
                if num_records > 0:
                    return num_records
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")

    def get_file_path(self):
        default_file = self.get_default_file()
        if default_file:
            use_default = input(f"Use default file ({os.path.join(self.input_folder, default_file)})? (y/n): ").lower().strip()
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
        try:
            files = [f for f in os.listdir(self.input_folder) if f.endswith('.txt')]
            return files[0] if files else None
        except FileNotFoundError:
            print(f"Input folder not found: {self.input_folder}")
            return None
        
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
    file_processor.process_file()
    csv_processor = CSVProcessor()
    csv_processor.process()