import xml.etree.ElementTree as ET
import os
import datetime
from manual_inputer.manual_inputer import NewsFeed
from csvp.main import CSVProcessor

class XMLProcessor:
    def __init__(self, news_feed, default_folder="news_feed/xml_processor/input_files"):
        self.news_feed = news_feed
        self.default_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), default_folder)
        
        os.makedirs(self.default_folder, exist_ok=True)

    def process_xml(self):
        num_records = self.get_num_records()
        file_path = self.get_file_path()
        
        if file_path is None:
            print("\nNo file to process.")
            return

        if not os.path.exists(file_path):
            print(f"\nFile not found: {file_path}")
            return

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            records = root.findall('record')
            self.process_records(records, num_records)

            print(f"Processed {min(num_records, len(records))} records from {file_path}")


            # os.remove(file_path)
            # print(f"File {file_path} has been removed after successful processing.")

        except ET.ParseError:
            print(f"Error: {file_path} is not a valid XML file.")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

    def get_num_records(self):
        while True:
            try:
                num_records = int(input("How many XML records do you want to parse? "))
                if num_records > 0:
                    return num_records
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")

    def get_file_path(self):
        default_file = self.get_default_xml_file()
        if default_file:
            use_default = input(f"Use default file ({os.path.join(self.default_folder, default_file)})? (y/n): ").lower().strip()
            if use_default == 'y':
                return os.path.join(self.default_folder, default_file)
        
        while True:
            file_path = input("Enter the path to the XML file: ").strip()
            if os.path.exists(file_path):
                return file_path
            else:
                print(f"File not found: {file_path}")
                retry = input("Do you want to try again? (y/n): ").lower().strip()
                if retry != 'y':
                    return None

    def get_default_xml_file(self):
        try:
            xml_files = [f for f in os.listdir(self.default_folder) if f.endswith('.xml')]
            return xml_files[0] if xml_files else None
        except FileNotFoundError:
            print(f"Default folder not found: {self.default_folder}")
            return None

    def process_records(self, records, num_records):
        processed_records = 0
        for record in records:
            if processed_records >= num_records:
                break
            self.process_record(record)
            processed_records += 1

    def process_record(self, record):
        record_type = record.get('type', '').lower()
        if record_type == 'news':
            text = record.find('text').text
            city = record.find('city').text
            self.news_feed.addRecord(self.news_feed.publishNews(text, city))
        elif record_type == 'ad':
            text = record.find('text').text
            expiration_date = record.find('expiration_date').text
            self.news_feed.addRecord(self.news_feed.publishAd(text, expiration_date))
        elif record_type == 'weather':
            city = record.find('city').text
            temperature = record.find('temperature').text
            conditions = record.find('conditions').text
            self.news_feed.addRecord(self.news_feed.publishWeather(city, temperature, conditions))
        else:
            print(f"Unknown record type: {record_type}")

# Output is in news_feed/output folder (due to newer tasks having one common file)
if __name__ == "__main__":
    news_feed = NewsFeed()
    xml_processor = XMLProcessor(news_feed)
    xml_processor.process_xml()
    csv_processor = CSVProcessor()
    csv_processor.process()