from bs4.builder import HTMLTreeBuilder
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import wget
import os


URL = "https://rare-pepe.com/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

pepes = []

def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))


# Load the figure elements with class 'gallery-item'
for image in soup.find_all("figure", class_='gallery-item'):
    # Grab next element
    divElement = image.find_next()
    # Grab next element
    aElement = divElement.find_next()
    # Find href image element
    link = aElement['href']
    # Open new BeautifulSoup
    nextPage = requests.get(link)
    newSoup = BeautifulSoup(nextPage.content, 'html.parser')
    #Find image with class 'aligncenter'
    for pepe in newSoup.find_all('img', class_='aligncenter'):
        imageLink = pepe['src']
        # Download image
        download(imageLink, 'images')
