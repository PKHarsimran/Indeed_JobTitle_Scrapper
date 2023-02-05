from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Initialize a webdriver instance
driver = webdriver.Firefox()

# Navigate to Indeed.com
driver.get("https://www.indeed.com/")

# Wait for the search bar element to appear and enter your search query
search_bar = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, "text-input-what")))
search_bar.send_keys("Software Engineer")

# Find the search button and click it
search_button = driver.find_element(By.CLASS_NAME,"yosegi-InlineWhatWhere-primaryButton")
search_button.click()

# Use Beautiful Soup to parse the HTML content of the page
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find all job listings on the page
job_listings = soup.find_all("div", class_="job_seen_beacon")

# Extract relevant information from each job listing
for job in job_listings:
    title = job.find("span", attrs={"id": lambda x: x and x.startswith("jobTitle-")})
    title = title.text
    company = job.find("span", class_="companyName").text
    location = job.find("div", class_="companyLocation").text
    print(f"{title} at {company} in {location}")

# Close the webdriver instance
driver.quit()
