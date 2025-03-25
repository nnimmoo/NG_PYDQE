
# Python for DQEs

This repository contains tasks from course 'Python for DQEs'.

### Task 1: Python Basics

create list of 100 random numbers, sort, calculate average(even and odd), print both average result. Located in folder: ***python basics***

### Task 2: Collections

Located in folder: ***collections***

### Task 3: String Object

Located in folder: ***strings***

### Task 4: Functions

Located in folder: ***functions***

### Task 5: Classes. OOP
Tool, which will do user generated news feed:
- User select what data type he wants to add
- Provides record type required data
- Record is published on text file in special format

**Available types of records:**

- News – text and city as input. Date is calculated during publishing.
- Private ad – text and expiration date as input. Day left is calculated during publishing.
- Weather Forecast - city, temperature and condition as text input.


Script Located in folder: ***news_feed / manual_inputer***

Output Located in folder: ***output***

### Task 6: Module. Files.
Expand news_feed with additional class, which allow to provide records by TXT file:
- Define your input format (one or many records)
- Default folder or user provided file path
- Remove file if it was successfully processed

Script Located in folder: ***news_feed / txt_processor***

Output Located in folder: ***output***

### Task 7: CSV Parsing
Expand news_feed with additional class, which allow to provide records by CSV file:
- Define your input format (one or many records)
- Default folder or user provided file path
- Remove file if it was successfully processed

Script Located in folder: ***news_feed / csvs***

Output Located in folder: ***output***

### Task 8: JSON Module
Expand news_feed with additional class, which allow to provide records by JSON file:
- Define your input format (one or many records)
- Default folder or user provided file path
- Remove file if it was successfully processed

Script Located in folder: ***news_feed / json_processor***

Output Located in folder: ***output***

### Task 9: XML Module
Expand news_feed with additional class, which allow to provide records by XML file:
- Define your input format (one or many records)
- Default folder or user provided file path
- Remove file if it was successfully processed

Script Located in folder: ***news_feed / xml_processor***

Output Located in folder: ***output***

### Task 10: Database API
Expand news_feed with additional class, which allows to save records in the database.
 - SQlite database allows us to save records in three different tables, according to their type.
 - With the new class integrated now in NewsFeed class, all the records added to database, no matter the input type.
 - No duplicate rows check, enables us to have unique records in the database.

 
Script Located in folder: ***news_feed / db_processor***
Database Located in folder: ***news_feed***

### Task 11: Final Task
Tool which calculates straight-line distance between different cities based on coordinates:
 1. User can provide two city names by console.
 2. If tool do not know about city coordinates, it will ask you for input and store it in SQLite database for future uses.
 3. Returns distance between cities in kilometers.

Script Located in folder: ***final_task***
Database Located in folder: ***final_task***

