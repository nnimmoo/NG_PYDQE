import datetime

class NewsFeed:
    def __init__(self, filename="News Feed.txt"):
        self.filename = filename

    def getUserInput(self, prompt):
        return input(prompt).strip()

    def publishNews(self, text=None, city=None):
        if text is None:
            text = self.getUserInput("Enter news text: ")
        if city is None:
            city = self.getUserInput("Enter city: ")
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        return f"--BREAKING NEWS--\n{text}\n{city}, {date}\n\n"

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
        
        return f"--AD--\n{text}\nExpiration date: {expiration_date}, {days_left} days left\n\n"

    def publishWeather(self, city=None, temperature=None, conditions=None):
        if city is None:
            city = self.getUserInput("Enter city: ")
        if temperature is None:
            temperature = self.getUserInput("Enter temperature (in Celsius): ")
        if conditions is None:
            conditions = self.getUserInput("Enter weather conditions: ")
        return f"--Weather Forecast-- \nCity: {city}\nTemperature: {temperature}*C\nWeather: {conditions}\n\n"

    def addRecord(self, record):
        with open(self.filename, "a") as file:
            file.write(record)
        print("Record added successfully!")

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