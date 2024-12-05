import os
from typing import List
from urllib.parse import urlparse

from ..data_extraction import load_urls

links_folder = "links"
data_folder = "data"
files_extension = "xlsx"


# Function to extract file name without extension
def get_file_name(url: str) -> str:
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    return os.path.splitext(file_name)[0]


def test_data_files_exists():
    links_path: str = os.path.join(os.getcwd(), links_folder)
    data_path: str = os.path.join(os.path.dirname(os.getcwd()), data_folder)

    data_urls: List[str] = load_urls(links_path)

    for url in data_urls:
        file_path: str = os.path.join(data_path, get_file_name(url))

        # handle the exceptional cases
        # 1. where a potentially url limitation causes the url to have PM25 instead of PM2.5 in it
        if "PM25" in file_path:
            file_path = file_path.replace("PM25", "PM2.5")

        # 2. file name in url might be versioned but the actual file name for the file in the zip is not versioned
        if "_v2" in file_path:
            file_path = file_path.replace("_v2", "")

        print("file path: ", file_path)
        assert os.path.exists(
            f"{file_path}.{files_extension}"
        ), f"File {file_path} does not exist!"
