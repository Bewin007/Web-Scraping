#Build2gether project scraping and story 1st para considered as intro

import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Function to scrape data from a given URL
def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    story_section = soup.find('section', id='story')
    
    # Extract and return content from the first <p> tag inside the <section>
    if story_section:
        first_p_tag = story_section.find('p')
        if first_p_tag:
            return first_p_tag.get_text()
    return None

# Base URL
base_url = 'https://www.hackster.io/'

# Open a CSV file in write mode
with open('output.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Text', 'URL', 'First_P_Tag_Content'])
    for page_number in range(1, 9):
        page_url = f'https://www.hackster.io/contests/buildtogether/submissions?page={page_number}#challengeNav'
        r = requests.get(page_url)

        print(r)
        soup = BeautifulSoup(r.content, 'html.parser')

        div_elements = soup.find_all('div', class_='card-body')

        # Iterate over each <div> element
        for div_element in div_elements:
            # Find all <h4> tags within the current <div>
            h4_tags = div_element.find_all('h4')

            # Iterate over each <h4> tag and find <a> tags within it
            for h4_tag in h4_tags:
                a_tags = h4_tag.find_all('a')
                for link in a_tags:
                    # Get the URL and text of the <a> tag
                    url = urljoin(base_url, link['href'])
                    text = link.text

                    # Scrape data from the linked page
                    first_p_content = scrape_data(url)

                    # Write the text, URL, and scraped data to the CSV file
                    csv_writer.writerow([text, url, first_p_content])
