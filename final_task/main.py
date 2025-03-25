import sqlite3
import math

class CityDistanceCalculator:
    def __init__(self, db_name='cities.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            name TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL
        )
        ''')
        self.conn.commit()

    def get_coordinates(self, city):
        self.cursor.execute('SELECT latitude, longitude FROM cities WHERE name = ?', (city,))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            print(f"City '{city}' not found in database. Please provide coordinates.")
            lat = float(input(f"Enter latitude for {city}: "))
            lon = float(input(f"Enter longitude for {city}: "))
            self.cursor.execute('INSERT INTO cities VALUES (?, ?, ?)', (city, lat, lon))
            self.conn.commit()
            return lat, lon

    def calculate_distance(self, city1, city2):
        lat1, lon1 = self.get_coordinates(city1)
        lat2, lon2 = self.get_coordinates(city2)

        # Convert latitude and longitude to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))

        # Radius of Earth in kilometers
        r = 6371

        return c * r

    def run(self):
        while True:
            city1 = input("Enter the name of the first city (or 'q' to exit): ").strip()
            if city1.lower() == 'q':
                break
            city2 = input("Enter the name of the second city: ").strip()

            distance = self.calculate_distance(city1, city2)
            print(f"The straight-line distance between {city1} and {city2} is {distance:.2f} km.")

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    calculator = CityDistanceCalculator()
    calculator.run()