import requests
from bs4 import BeautifulSoup
import re
import csv
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def get_last_page_number(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    paginator = soup.find('ul', class_='paginator_container__DHWL2')
    last_page = paginator.find_all('li', class_='paginator_page__O0uBD')[-1]
    return int(last_page.text)

def scrape_agents(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    agents = soup.find_all('div', class_='agents_agent___NyXQ')

    results = []
    for agent in agents:
        name_elem = agent.find('h2', class_='agents_name__jvXyG')
        name = name_elem.text if name_elem else 'N/A'

        phone_elem = agent.find('div', class_='agents_phone__mK5H7')
        phone = phone_elem.text.strip() if phone_elem else 'N/A'
        phone = re.sub(r'^.*?\)', '', phone).strip()  # Remove SVG text

        email_elem = agent.find('div', class_='agents_email__CAPFo')
        email = email_elem.text.strip() if email_elem else 'N/A'
        email = re.sub(r'^.*?\)', '', email).strip()  # Remove SVG text

        results.append({
            'name': name,
            'phone': phone,
            'email': email
        })

    return results

def save_to_csv(agents, filename):
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'phone', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()  # Write header only if the file is newly created
        
        for agent in agents:
            writer.writerow(agent)

def main():
    base_url = 'https://www.residential.com/real_estate_agents/FL?page=1'
    last_page = get_last_page_number(base_url)
    print(f"Total pages: {last_page}")

    csv_filename = 'real_estate_agents.csv'

    for page in range(1, last_page + 1):
        print(f"Scraping page {page}/{last_page}")
        url = f"{base_url}?page={page}"
        agents = scrape_agents(url)
        
        save_to_csv(agents, csv_filename)
        print(f"Data from page {page} appended to {csv_filename}")

    print(f"Scraping completed. All data saved to {csv_filename}")

if __name__ == "__main__":
    main()