from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

# Set options for the webdriver
options = Options()
options.add_argument("--user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'")

# Initialize a Selenium webdriver
driver = webdriver.Firefox()

# Visit the Indeed website
driver.get("https://www.indeed.com/")

# Find the search bar and enter a job search query
search_bar = driver.find_element(By.NAME, "q")
search_bar.send_keys("data scientist")

# Submit the search query
search_bar.submit()

# Wait for the page to load
driver.implicitly_wait(10)

# Scrape the job listings
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
results_list = soup.find("ul", class_="jobsearch-ResultsList css-0")
job_listings_title = results_list.find_all("li", class_="jobsearch-SerpJobCard")

# Close the browser
driver.quit()
