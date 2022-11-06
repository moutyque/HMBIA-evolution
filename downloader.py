import os
from datetime import date
from pathlib import Path
from urllib.parse import urljoin
from waybackpy import WaybackMachineCDXServerAPI
import requests as requests
from bs4 import BeautifulSoup
import concurrent.futures
from concurrent.futures import wait

class PDF_Image_Downloader:
    def __init__(self, base_url, base_path):
        "Constructor: Initialises file1 and file 2"
        self.download_dir = base_path
        self.base_url = base_url

    def __download_from_url(self, when=date.today().strftime("%d/%m/%Y")):
        # If there is no such folder, the script will create one automatically
        folder_location = fr'{self.download_dir}/{when}'
        if not os.path.exists(folder_location): os.makedirs(folder_location)

        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, "html.parser")
        self.__export(folder_location, soup, self.base_url, ".pdf")
        self.__export(folder_location, soup, self.base_url, ".jpg")

    def __export_tag(self, folder_location, soup, url, extension, tag, attribute):
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

    def __export(self, folder_location, soup, url, extension):
        self.__export_tag(folder_location, soup, url, extension, "div", "data-wts-url")
        self.__export_tag(folder_location, soup, url, extension, "a", "href")

    def download_current_version(self):
        self.__download_from_url()

    def download_past_version(self):
        user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
        cdx = WaybackMachineCDXServerAPI(self.base_url, user_agent, start_timestamp="2020", end_timestamp="2022")
        futures = [concurrent.futures.ThreadPoolExecutor(max_workers=4).submit(self.__download_from_url, item.archive_url,
                                                                               item.datetime_timestamp.strftime(
                                                                                   "%Y_%m_%d"))
                   for item in cdx.snapshots()]
        wait(futures)  # ALL_COMPLETED is actually the default
