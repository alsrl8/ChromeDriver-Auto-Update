import shutil
import subprocess
import zipfile

import requests
import os


def get_chromedriver_path():
    return './driver/chromedriver.exe'


def get_chromedriver_zip_path():
    return './driver/chrome-win64.zip'


def get_latest_chromedriver_version():
    url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_stable = data['channels']['Stable']
        latest_stable_version = latest_stable['version']
        return latest_stable_version
    else:
        print("Failed to fetch latest version")
        return None


def get_chromedriver_version(driver_path) -> (str, Exception):
    try:
        result = subprocess.run([driver_path, '--version'], capture_output=True, text=True)
        version_info = result.stdout.strip().split()[1]
        return version_info, None
    except Exception as e:
        return '', e


def check_if_update_needed(current_version):
    latest_version = get_latest_chromedriver_version()
    if latest_version is None:
        return False
    return current_version.split('.')[0] != latest_version.split('.')[0]


def update_chromedriver():
    url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_stable = data['channels']['Stable']
        download_infos = latest_stable['downloads']['chromedriver']
        for info in download_infos:
            if info['platform'] != 'win64':
                continue
            response = requests.get(info['url'])
            if response.status_code == 200:
                driver_zip_path = download_chromedriver_zip_file(response)
                print(f'Downloaded chromedriver zip file to {driver_zip_path}')

                unzip_chromedriver_zip_file(driver_zip_path)
                print(f'Unzipped chromedriver zip file')

                destination_path = move_extracted_driver()
                print(f'ChromeDriver updated and moved to {destination_path}')

                os.remove(driver_zip_path)
                print(f'Removed the zip file at {driver_zip_path}')

                extracted_directory_path = remove_unzipped_directory()
                print(f'Removed the extracted directory at {extracted_directory_path}')
            break
    else:
        print('Failed to fetch latest version')
        return None


def remove_unzipped_directory():
    extracted_directory_path = './driver/chromedriver-win64'
    shutil.rmtree(extracted_directory_path)
    return extracted_directory_path


def download_chromedriver_zip_file(response):
    driver_zip_path = get_chromedriver_zip_path()
    with open(driver_zip_path, 'wb') as file:
        file.write(response.content)
    return driver_zip_path


def unzip_chromedriver_zip_file(driver_zip_path):
    with zipfile.ZipFile(driver_zip_path, 'r') as zip_ref:
        zip_ref.extractall('./driver/')


def move_extracted_driver():
    extracted_driver_path = './driver/chromedriver-win64/chromedriver.exe'
    destination_path = get_chromedriver_path()
    shutil.move(extracted_driver_path, destination_path)
    return destination_path


def check_and_update_chromedriver():
    driver_path = get_chromedriver_path()
    chromedriver_version, error = get_chromedriver_version(driver_path)
    if error:
        if isinstance(error, FileNotFoundError):
            print('Chromedriver not found at the specified path. Proceeding with update...')
            update_chromedriver()
        else:
            print(f'An unexpected error occurred: {error}')
        return

    if check_if_update_needed(chromedriver_version):
        print('Chromedriver is outdated. Updating...')
        update_chromedriver()
    else:
        print('Your Chromedriver is up to date.')
