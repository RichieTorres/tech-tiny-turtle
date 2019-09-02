from pathlib import Path
import shutil
import hashlib
import json
import os
import tarfile
import urllib.request
from shutil import copytree, rmtree

DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

HOME_DIR = str(Path.home())
CACHE_FOLDER = os.path.join(HOME_DIR, '.cache', 'ttt')
OPT_FOLDER = os.path.join(HOME_DIR, '.local', 'opt')
ENTRY_FOLDER = os.path.join(HOME_DIR, '.local', 'share', 'applications')
BIN_FOLDER = os.path.join(HOME_DIR, '.local', 'bin')


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

    extract_file(file_name, p, data['extract_with_folder'])
    link_bin_folder(p)


def download_file(url, original_md5sum):
    # Download the file from `url` and save it locally under `file_name`:
    file_name = os.path.join(CACHE_FOLDER, os.path.basename(url))

    md5sum = None
    if os.path.exists(file_name):
        md5sum = hashlib.md5(open(file_name, 'rb').read()).hexdigest()

    if original_md5sum == md5sum:
        print('Found in cache')
    else:
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            data = response.read()  # a `bytes` object
            out_file.write(data)
    return file_name


def create_desktop_entry(package_name, entry):
    package_folder = os.path.join(OPT_FOLDER, package_name)
    with open(os.path.join(ENTRY_FOLDER, f'{package_name}.desktop'), 'w') as out_file:
        out_file.write(entry.format(OPT_FOLDER=package_folder))


def extract_file(file_name, package_name, extract_with_folder=False):
    final_folder = os.path.join(OPT_FOLDER, package_name)
    tmp_folder = os.path.join('/tmp/', package_name)
    dest = tmp_folder if extract_with_folder else final_folder

    if os.path.isdir(final_folder):
        rmtree(final_folder)
    if os.path.isdir(tmp_folder):
        rmtree(tmp_folder)

    tar = tarfile.open(file_name)
    tar.extractall(dest)
    tar.close()

    if extract_with_folder:
        inner_folder = None
        for r in os.listdir(tmp_folder):
            inner_folder = os.path.join(tmp_folder, r)
        shutil.move(inner_folder, final_folder)


def link_bin_folder(package_name):
    package_bin_folder = os.path.join(OPT_FOLDER, package_name, 'bin')
    if os.path.isdir(package_bin_folder):
        for f in os.listdir(package_bin_folder):
            os.symlink( os.path.join(package_bin_folder, f), os.path.join(BIN_FOLDER, f))
