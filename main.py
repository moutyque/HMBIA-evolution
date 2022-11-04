import os
from datetime import date
from pathlib import Path
from urllib.parse import urljoin
from waybackpy import WaybackMachineCDXServerAPI
import requests as requests
from bs4 import BeautifulSoup
import concurrent.futures
from concurrent.futures import wait

def download_from_url(url, when=date.today().strftime("%d/%m/%Y")):
    # If there is no such folder, the script will create one automatically
    folder_location = fr'./webscraping/{when}'
    if not os.path.exists(folder_location): os.makedirs(folder_location)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    export(folder_location, soup, url, ".pdf")
    export(folder_location, soup, url, ".jpg")


def export_tag(folder_location, soup, url, extension, tag, attribute):
    for link in soup.select(f"{tag}[{attribute}$='{extension}']"):
        # Name the pdf files using the last portion of each link which are unique in this case
        filename = os.path.join(folder_location, link[f'{attribute}'].split('/')[-1])
        join_url = urljoin(url, link[f'{attribute}'])
        try:
            info = requests.head(join_url, allow_redirects=True)
            same_size = False
            if Path(filename).is_file():
                with open(filename, 'rb') as f:
                    same_size = len(f.read()) == info.headers.get('Content-Length', -1)
            if not same_size:
                print(f'Writing {filename}')
                resp = requests.get(join_url)
                with open(filename, 'wb') as f:
                    f.write(resp.content)
                    print(os.path.getsize(filename))
        except ConnectionError:
            print("ERROR")


def export(folder_location, soup, url, extension):
    export_tag(folder_location, soup, url, extension, "div", "data-wts-url")
    export_tag(folder_location, soup, url, extension, "a", "href")


def download_current_version(url):
    download_from_url(url)


def download_past_version(url):
    user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
    cdx = WaybackMachineCDXServerAPI(url, user_agent, start_timestamp="2020", end_timestamp="2022")
    futures = [concurrent.futures.ThreadPoolExecutor(max_workers=4).submit(download_from_url, item.archive_url,
                                                                           item.datetime_timestamp.strftime("%Y_%m_%d"))
               for item in cdx.snapshots()]
    wait(futures)  # ALL_COMPLETED is actually the default


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = "https://hmbia.info/rules-and-regulations/"
    download_past_version(url)
# download_current_version(url)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
