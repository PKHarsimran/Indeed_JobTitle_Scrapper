import click
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Dictionary of available webdriver classes
DRIVER_CLASSES = {
    'Firefox': webdriver.Firefox,
    'Chrome': webdriver.Chrome,
    'Safari': webdriver.Safari,
    'Edge': webdriver.Edge,
}

# Create a click command line interface
@click.command()
# Add an option for user to select webdriver
@click.option('--driver', type=click.Choice(DRIVER_CLASSES.keys()), prompt='Select the webdriver to use', help='WebDriver to use')
# Add an option for user to provide search query
@click.option('--search-query', prompt='Enter the search query', help='The query to search for on indeed.com')
def scrape_indeed(driver, search_query):
    """
    This function scrapes job information from indeed.com using the selected webdriver.
    """
    # Get the selected driver class
    DriverClass = DRIVER_CLASSES[driver]
    # Initialize the driver
    driver = DriverClass()
    # Navigate to indeed.com
    driver.get("https://www.indeed.com/")
    # Wait for the search bar to load
    search_bar = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, "text-input-what")))
    # Enter the search query into the search bar
    search_bar.send_keys(search_query)
    # Find and click the search button
    search_button = driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
    search_button.click()
    # Parse the page source into a BeautifulSoup object
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Find all job listings on the page
    job_listings = soup.find_all("div", class_="job_seen_beacon")
    # Print the title, company, and location for each job listing
    for job in job_listings:
        title = job.find("span", attrs={"id": lambda x: x and x.startswith("jobTitle-")})
        title = title.text
        company = job.find("span", class_="companyName").text
        location = job.find("div", class_="companyLocation").text
        print(f"{title} at {company} in {location}")
    # Close the webdriver
    driver.quit()

if __name__ == '__main__':
    scrape_indeed()
