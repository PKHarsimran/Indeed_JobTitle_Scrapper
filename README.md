Indeed Job Scraper

This code scrapes job information from Indeed.com, a popular job search website.
Requirements

    Selenium
    Beautiful Soup
    geckodriver

Usage

    Install the required packages using pip:

pip install selenium beautifulsoup4

    Download the latest version of geckodriver and place it in your PATH, e.g., place it in /usr/bin or /usr/local/bin.

    Clone this repository:

bash

git clone https://github.com/[username]/indeed-job-scraper

    Navigate to the directory:

bash

cd indeed-job-scraper

    Run the script using the following command:

python indeed-scraper.py

    The script will open a firefox window and scrape job information from Indeed.com. The extracted information will be printed in the console.

Output

The script outputs the following information for each job listing on the page:

    Job title
    Company name
    Location

Limitations

The code is limited to the first page of job listings on Indeed.com. To scrape additional pages, you will need to modify the code.
License

This project is licensed under the MIT License.
