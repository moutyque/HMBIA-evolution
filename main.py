import os

from comparator import PDF_Image_Compare
from downloader import PDF_Image_Downloader
from os.path import exists
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = "https://hmbia.info/rules-and-regulations/"
    base_path = "./webscraping"
    # PDF_Image_Downloader(url, base_path).download_past_version()

    list_subfolders_with_paths = [f.path for f in os.scandir(base_path) if f.is_dir()]
    list_subfolders_with_paths.sort()
    for index in range(0, list_subfolders_with_paths.__sizeof__() - 1):
        list_files = [f.path for f in os.scandir(list_subfolders_with_paths[index]) if f.is_file()]
        for ref_file in list_files:
            path = f'{list_subfolders_with_paths[index+1]}/{os.path.basename(ref_file)}'
            if exists(path):
                test_obj = PDF_Image_Compare(pdf1=os.path.abspath(ref_file), pdf2=os.path.abspath(path))
                result_flag = test_obj.get_pdf_diff()
                if result_flag == True:
                    print('The two PDF matched properly')
                else:
                    print('The PDFs didnt match properly, check the diff file generated')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
