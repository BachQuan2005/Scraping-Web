from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin

def save_text_to_file(text, filename):
    with open(filename, "w", encoding = "utf-8") as file:
        file.write(text)

def save_image_from_url(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    image_name = os.path.join(folder, url.split("/")[-1])
    
    img_data = requests.get(url).content
    with open(image_name, 'wb') as handler:
        handler.write(img_data)

def website_to_scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    paragraphs =  soup.find_all('p')
    all_text = "\n".join([para.get_text() for para in paragraphs])

    paragraphs_2 = soup.find_all('a')
    all_text_2 = "\n".join([para_2.get_text() for para_2 in paragraphs_2])

    image_urls = [urljoin(url, img['src']) for img in soup.find_all('img', src=True)]
    
    return all_text,all_text_2, image_urls

url = "https://ptit.edu.vn/"

all_text,all_text_2, image_urls = website_to_scrape(url)

if all_text:
    save_text_to_file(all_text, 'web_paragraph.txt')
    print("text has been saved to 'web_paragraph.txt'.")

if all_text_2:
    save_text_to_file(all_text_2, 'web_paragraph_2.txt')
    print("Text has been saved to 'web_paragraph_2.txt'.")

if image_urls:
    for image_url in image_urls:
        save_image_from_url(image_url, 'images')
    print("Images have been saved in the 'images' folder.")


