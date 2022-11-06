from downloader import PDF_Image_Downloader

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = "https://hmbia.info/rules-and-regulations/"
    base_path = "./webscraping"
    PDF_Image_Downloader(url, base_path).download_past_version()
    # download_past_version(url)
    # download_current_version(url)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
