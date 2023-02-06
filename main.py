import click
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

@click.command()
@click.option("--query", prompt="Enter search query")
def main(query):
    # Initialize a webdriver instance to open a web browser (Firefox in this case)
    driver = webdriver.Firefox()

    # Navigate to the Indeed website
    driver.get("https://www.indeed.com/")

    # Wait for the search bar element to appear, and then enter the search query
    # The WebDriverWait method is used to wait for a specific element to appear on the page
    # The presence_of_element_located method is used to wait for an element to be present on the page
    # The ID locator strategy is used to locate the search bar element
    search_bar = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, "text-input-what")))

    # Enter the search query into the search bar
    search_bar.send_keys(query)

    # Locate the search button and click it
    # The CLASS_NAME locator strategy is used to locate the search button element
    search_button = driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
    search_button.click()

    # Parse the HTML content of the page using Beautiful Soup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find all job listings on the page
    # The find_all method is used to find all elements that match the specified criteria
    # The class_ attribute is used to specify the CSS class name to search for
    job_listings = soup.find_all("div", class_="job_seen_beacon")

    # Loop through each job listing and extract relevant information
    for job in job_listings:
        # Extract the job title
        # The find method is used to find the first element that matches the specified criteria
        # The attrs attribute is used to specify the attributes to search for
        # The lambda function is used to filter the elements based on the attribute value
        title = job.find("span", attrs={"id": lambda x: x and x.startswith("jobTitle-")})
        # Extract the text of the job title element
        title = title.text
        # Extract the company name
        company = job.find("span", class_="companyName").text
        # Extract the location
        location = job.find("div", class_="companyLocation").text
        # Print the job title, company name, and location
        print(f"{title} at {company} in {location}")

    # Close the webdriver instance and the web browser
    driver.quit()

if __name__ == "__main__":
    main()