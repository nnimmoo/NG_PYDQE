import os
import sys

# Get the path to the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))
# Add the project root directory to the Python path
sys.path.append(project_root)

from manual_inputer.manual_inputer import NewsFeed
from txt_processor.txt_processor import TXTFileProcessor
from json_processor.json_processor import JSONProcessor
from xml_processor.xml_processor import XMLProcessor

class MainRunner:
    def __init__(self):
        self.news_feed = NewsFeed()
        self.txt_processor = TXTFileProcessor(self.news_feed)
        self.json_processor = JSONProcessor(self.news_feed)
        self.xml_processor = XMLProcessor(self.news_feed)

    def run(self):
        while True:
            print("\nSelect an option:")
            print("1. Manual input")
            print("2. Process TXT file")
            print("3. Process JSON file")
            print("4. Process XML file")
            print("5. Exit")
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                self.news_feed.run()
            elif choice == '2':
                self.txt_processor.process_file()
            elif choice == '3':
                self.json_processor.process_json()
            elif choice == '4':
                self.xml_processor.process_xml()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

        print("Thank you for using the News Feed system! Till Later ^^")

if __name__ == "__main__":
    runner = MainRunner()
    runner.run()