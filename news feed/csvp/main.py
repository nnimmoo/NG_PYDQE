import csv
import os
import string
import re
from collections import Counter

class CSVProcessor:
    def __init__(self, input_file="News Feed.txt", output_folder="output"):
        # Get the absolute path of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one directory to get to the project root
        project_root = os.path.dirname(script_dir)
        
        self.input_file = os.path.join(project_root, output_folder, input_file)
        self.output_folder = os.path.join(project_root, output_folder)
        self.word_count_file = os.path.join(self.output_folder, "word_count.csv")
        self.letter_count_file = os.path.join(self.output_folder, "letter_count.csv")

    def process(self):
        print(f"Looking for input file: {self.input_file}")
        if not os.path.exists(self.input_file):
            print(f"Input file not found: {self.input_file}")
            return

        print("Reading input file...")
        with open(self.input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        print(f"Content length: {len(content)}")
        print("Creating word count CSV...")
        self.create_word_count_csv(content)
        print("Creating letter count CSV...")
        self.create_letter_count_csv(content)
        print("Processing complete.")

    def create_word_count_csv(self, content):
        words = re.findall(r"\b[a-z]+(?:'[a-z]+)?\b", content.lower())
        word_count = Counter(words)
        
        with open(self.word_count_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['word', 'count'])
            for word, count in word_count.items():
                writer.writerow([word, count])

    def create_letter_count_csv(self, content):
        letter_count = Counter(char.lower() for char in content if char.isalpha())
        total_letters = sum(letter_count.values())
        uppercase_count = sum(1 for char in content if char.isupper())

        with open(self.letter_count_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['letter', 'count_all', 'count_uppercase', 'percentage'])
            for letter in string.ascii_lowercase:
                count_all = letter_count[letter]
                count_uppercase = sum(1 for char in content if char.lower() == letter and char.isupper())
                percentage = (count_all / total_letters) * 100 if total_letters > 0 else 0
                writer.writerow([letter, count_all, count_uppercase, f"{percentage:.2f}%"])

def main():
    processor = CSVProcessor()
    processor.process()

if __name__ == "__main__":
    main()