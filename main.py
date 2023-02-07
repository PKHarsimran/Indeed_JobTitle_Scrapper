import click
import openpyxl
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Keys
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
@click.option('--search-location', prompt='Enter the location eg - Any or Remote', help='Location to search from indeed.com. Format: City, Country or Remote')
def scrape_indeed(driver, search_query, search_location):
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
    #Wait for Location search bar to load
    location_bar = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, "text-input-where")))
    # Enter the Location query into the Location bar
    location_bar.send_keys(Keys.CONTROL + "a")
    location_bar.send_keys(Keys.BACKSPACE)
    location_bar.send_keys(search_location)
    # Find and click the search button
    search_button = driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
    search_button.click()
    # Parse the page source into a BeautifulSoup object
    soup = BeautifulSoup(driver.page_source, "html.parser")

    #Check to see if there more results

    Navigation_bar_present = False
    try:
        Navigation_bar = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, '//nav[@role="navigation"]')))
        Navigation_bar_present = True
    except:
        Navigation_bar_present = False

    # Find all job listings on the page
    job_listings = soup.find_all("div", class_="job_seen_beacon")

    # Create an empty dataframe to store job information
    job_data = pd.DataFrame(columns=['Title', 'Company', 'Location'])

    # Create a new Excel file if it doesn't already exist
    try:
        workbook = openpyxl.load_workbook("job_data.xlsx")
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
        workbook.save("job_data.xlsx")

    # Print the title, company, and location for each job listing
    for job in job_listings:
        title = job.find("span", attrs={"id": lambda x: x and x.startswith("jobTitle-")})
        title = title.text
        company = job.find("span", class_="companyName").text
        location = job.find("div", class_="companyLocation").text
        print(f"{title} at {company} in {location}")
        temp_df = pd.DataFrame({'Title': [title], 'Company': [company], 'Location': [location]})
        job_data = pd.concat([job_data, temp_df], ignore_index=True)

    # Write the data to an Excel workbook
    try:
        writer = pd.ExcelWriter('job_data.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace')
    except ValueError:
        writer = pd.ExcelWriter('job_data.xlsx', engine='openpyxl', mode='a', if_sheet_exists='fail')
        print("Sheet with that name already exists.")
    job_data.to_excel(writer, sheet_name=search_query, index=False)
    writer.close()

    driver.quit()

if __name__ == '__main__':
    scrape_indeed()
