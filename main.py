import click
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

DRIVER_CLASSES = {
    'Firefox': webdriver.Firefox,
    'Chrome': webdriver.Chrome,
    'Safari': webdriver.Safari,
    'Edge': webdriver.Edge,
}

@click.command()
@click.option('--driver', type=click.Choice(DRIVER_CLASSES.keys()), default='Firefox', help='WebDriver to use')
@click.option('--search-query', prompt='Enter the search query', help='The query to search for on indeed.com')
def scrape_indeed(driver, search_query):
    DriverClass = DRIVER_CLASSES[driver]
    driver = DriverClass()
    driver.get("https://www.indeed.com/")
    search_bar = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, "text-input-what")))
    search_bar.send_keys(search_query)
    search_button = driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
    search_button.click()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_listings = soup.find_all("div", class_="job_seen_beacon")
    for job in job_listings:
        title = job.find("span", attrs={"id": lambda x: x and x.startswith("jobTitle-")})
        title = title.text
        company = job.find("span", class_="companyName").text
        location = job.find("div", class_="companyLocation").text
        print(f"{title} at {company} in {location}")
    driver.quit()

if __name__ == '__main__':
    scrape_indeed()
