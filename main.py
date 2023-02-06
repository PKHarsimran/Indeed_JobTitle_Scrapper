import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def extract_job_info(soup):
    job_listings = soup.find_all("div", class_="job_seen_beacon")
    for job in job_listings:
        title = job.find("span", attrs={"id": lambda x: x and x.startswith("jobTitle-")})
        title = title.text
        company = job.find("span", class_="companyName").text
        location = job.find("div", class_="companyLocation").text
        print(f"{title} at {company} in {location}")


def main(args):
    # Initialize the specified webdriver instance
    if args.webdriver == "firefox":
        driver = webdriver.Firefox()
    elif args.webdriver == "chrome":
        driver = webdriver.Chrome()
    else:
        raise ValueError("Invalid webdriver type. Choose either 'firefox' or 'chrome'.")

    driver.get("https://www.indeed.com/")

    search_bar = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.ID, "text-input-what"))
    )
    search_bar.send_keys(args.search_query)

    search_button = driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
    search_button.click()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    extract_job_info(soup)

    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape job information from Indeed.")
    parser.add_argument("search_query", type=str, help="Search query to send to Indeed.")
    parser.add_argument("webdriver", type=str, help="Type of webdriver to use.",
                        choices=["firefox", "chrome"])
    args = parser.parse_args()
    main(args)
