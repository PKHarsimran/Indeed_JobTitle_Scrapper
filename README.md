# Job Scraper using Selenium and Beautiful Soup

A simple Python script that scrapes job listings from the Indeed website using Selenium and Beautiful Soup.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need the following libraries installed:

    click
    openpyxl
    pandas
    selenium
    bs4

You can install them using pip with the following command:

        pip install selenium <library name for example:  pip install selenium bs4 >
        
### Running the script

Clone this repository to your local machine and run the script using Python:

        python scrape_indeed.py --driver [DriverClass] --search-query [search-query] --search-location [search-location]

Options

--driver (required) - The webdriver to use. Can be one of the following: Firefox, Chrome, Safari, or Edge.

--search-query (required) - The query to search for on indeed.com.

--search-location (required) - The location to search from indeed.com. Can be in the format of a city and country or Remote.

The script uses the selected webdriver to navigate to indeed.com, enter the search query and location, and scrape job information from the results page. The job information is then printed to the console and stored in an Excel workbook. If a workbook with the same name already exists, the data is appended to the existing workbook.

## Built With

- [Selenium](https://selenium-python.readthedocs.io/) - A web testing framework used to automate web browsers
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - A library used to extract data from HTML and XML files
- [Click](https://click.palletsprojects.com/en/7.x/) - a Python library for creating beautiful and user-friendly command line interfaces.
- [pandas](https://pandas.pydata.org/) - a library in Python used for data analysis and manipulation, providing high-performance, easy-to-use data structures and data analysis tools.
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/) - "openpyxl" is a library for reading and writing Excel 2010 files (i.e. .xlsx) using the openpyxl module.

