#!/usr/bin/env python3

from os import mkdir, path, symlink
from pathlib import Path
from shutil import copytree, rmtree

HOME_DIR = str(Path.home())

MAIN_FILE = './ttt.py'
CACHE_FOLDER = path.join(HOME_DIR, '.cache')
CACHE_TTT_FOLDER = path.join(CACHE_FOLDER, 'ttt')
LOCAL_FOLDER = path.join(HOME_DIR, '.local')
BIN_FOLDER = path.join(LOCAL_FOLDER, 'bin')
SHARE_FOLDER = path.join(LOCAL_FOLDER, 'share')
OPT_FOLDER = path.join(LOCAL_FOLDER, 'opt')
TTT_FOLDER = path.join(SHARE_FOLDER, 'TTT')

# Create folders
REQUIRED_FOLDERS = [LOCAL_FOLDER, BIN_FOLDER,
                    SHARE_FOLDER, OPT_FOLDER, CACHE_TTT_FOLDER]
for f in REQUIRED_FOLDERS:
    if not path.isdir(f):
        print(f'creating folder {f}')
        mkdir(f)

# Copy files
if path.isdir(TTT_FOLDER):
    rmtree(TTT_FOLDER)
copytree('.', TTT_FOLDER)

# Set exe
if not path.exists(path.join(BIN_FOLDER, 'ttt')):
    symlink(path.join(TTT_FOLDER, MAIN_FILE), path.join(BIN_FOLDER, 'ttt'))
