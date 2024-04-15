# Books To Scrape Sandbox

A fictional bookstore that desperately wants to be scraped. It's a safe place for beginners learning web scraping and for developers validating their scraping technologies as well.

|Details              |        |
|:--                  |:--     |
| Amount of items     | 1000   |
| Pagination          | ✔      |
| Items per page      | max 20 |
| Requires JavaScript | ✘      |

 There are following information that can be scraped...
 
- Book UPC ID
- Book Title
- Book Price
- Book Tag
- Number of Books Available
- Book Review

# How to Run?

1.  Clone this repository.

	```
	git clone https://github.com/VIIVIIIIX/books-to-scrape-sandbox.git
	```

2. Create a virtual environment.

	```
	cd books-to-scrape-sandbox
	python3 -m venv .venv
	```

3. Activate the virtual environment and install necessary libraries.

	```
	cd .venv
	source ./bin/activate
	cd ..
	pip install -r requirements.txt
	```

4. Change the directory and run the code to generate the csv containing data.
	
	```
	cd books-async
	python3 books.py
	```
