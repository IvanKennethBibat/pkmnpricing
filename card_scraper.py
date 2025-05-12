import requests
from bs4 import BeautifulSoup
import os
import urllib
from urllib.parse import urljoin

def scrape_card_images(url, div_selector):
    """
    Scrapes card images from a specific div on a webpage
    
    Args:
        url (str): The URL of the webpage to scrape
        div_selector (str): CSS selector for the div containing card images
        
    Returns:
        list: List of image URLs found in the specified div
    """
    folder_path = r"C:\Users\Ivan\Documents\GitHub\pkmnpricing\pkmnpricing\card_images"
    
    # Send GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    

    j = 1


    # Find all images in site in div class entry-content
    entries = soup.find_all('div', {'class':'entry-content'})  # Using exact class name
    if not entries:
        return []
    
    card_urls = []
    for entry in entries:
        card_urls.append(entry.a('href'))
        print(j)
        j += 1

    for entry_url in card_urls:
        response = requests.get(entry_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        card_image_url = soup.find("div", {"class":"card-image"}).a['href']
        filename = os.path.basename(card_image_url)

        filepath = os.path.join(folder_path, filename)
        urllib.request.urlretrieve(card_image_url, filepath)
        
        print(f"Downloaded {filename} to {filepath}")
    return print("Done")

if __name__ == "__main__":
    target_url = "https://pkmncards.com/set/prismatic-evolutions/"
    div_selector = "div.entry-content"
    
    print(scrape_card_images(target_url, div_selector))

