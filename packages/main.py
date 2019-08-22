import os
from pathlib import Path
import json
import urllib.request
import hashlib
import tarfile

DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

HOME_DIR = str(Path.home())
CACHE_FOLDER = os.path.join(HOME_DIR, '.cache', 'ttt')
OPT_FOLDER = os.path.join(HOME_DIR, '.local', 'opt')
ENTRY_FOLDER = os.path.join(HOME_DIR, '.local', 'share', 'applications')


def download_file(url, original_md5sum):
    # Download the file from `url` and save it locally under `file_name`:
    file_name = os.path.join(CACHE_FOLDER, os.path.basename(url))

    md5sum = None
    if os.path.exists(file_name):
        md5sum = hashlib.md5(open(file_name, 'rb').read()).hexdigest()

    if not original_md5sum == md5sum:
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            data = response.read()  # a `bytes` object
            out_file.write(data)
    return file_name


def install(p):
    json_filename = os.path.join(DATA_FOLDER, f'{p}.json')
    if not os.path.exists(json_filename):
        print(f'package {p} not found')
        return

    with open(json_filename) as json_file:
        data = json.load(json_file)
    name = data['name']

    base_url = data['base_url']
    versions = data['versions']
    md5sum = data['md5sum']
    latest_version = versions[0]
    url = base_url.format(version=latest_version)

    if 'entry' in data:
        create_desktop_entry(p, data['entry'])

    print(f'Installing {name}')
    print(f'Downloading {url}')
    file_name = download_file(url, md5sum)

    tar = tarfile.open(file_name)
    tar.extractall(os.path.join(OPT_FOLDER, p))
    tar.close()


def create_desktop_entry(package_name, entry):
    package_folder = os.path.join(OPT_FOLDER, package_name)
    with open(os.path.join(ENTRY_FOLDER, f'{package_name}.desktop'), 'w') as out_file:
        out_file.write(entry.format(OPT_FOLDER=package_folder))
