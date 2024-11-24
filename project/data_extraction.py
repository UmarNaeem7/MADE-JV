import io
import os
import zipfile
from typing import List

import requests
from tenacity import retry, stop_after_attempt, wait_fixed

links_folder = "links"
data_folder = "data"


def load_urls(links_path: str) -> List[str]:
    urls = []

    for filename in os.listdir(links_path):
        file_path = os.path.join(links_path, filename)

        if os.path.isfile(file_path):
            print(f"Reading file: {filename}")

            with open(file_path, "r") as file:
                for url in file:
                    urls.append(url.strip())
                    print(url.strip())

    return urls


@retry(wait=wait_fixed(3), stop=stop_after_attempt(3))
def load_save_data(url: str, data_path: str):
    response = requests.get(url)
    if response.status_code == 200:
        if url.endswith(".zip"):
            try:
                with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                    z.printdir()

                    # Find the Excel file from the zip & save it to the data directory
                    for file_name in z.namelist():
                        if file_name.endswith(".xlsx"):
                            output_path = os.path.join(data_path, file_name)
                            with open(output_path, "wb") as f:
                                f.write(z.read(file_name))
                            print(f"Saved {file_name} to {output_path}")
                            break
            except zipfile.BadZipFile:
                print(
                    f"Error: The file at {url} is not a valid ZIP file or is corrupted."
                )
        else:
            # If the URL points to a single file (e.g., .xlsx or .csv)
            file_name = os.path.basename(url)
            output_path = os.path.join(data_path, file_name)

            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Saved {file_name} to {output_path}")
    else:
        print(f"Alert!!! Failed to download the file from {url}")


def main():
    # define paths to read from & write data to
    links_path: str = os.path.join(os.getcwd(), links_folder)
    data_path: str = os.path.join(os.path.dirname(os.getcwd()), data_folder)

    # fetch the pre-defined urls for the datasets
    data_urls: List[str] = load_urls(links_path)

    # save dataset from each url to the data folder
    for url in data_urls:
        try:
            load_save_data(url, data_path)
        except Exception as e:
            print(f"Operation load_save_data failed after retries: {e}")


if __name__ == "__main__":
    main()
