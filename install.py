#!/usr/bin/env python

import configparser
from pathlib import Path
import subprocess
import os
import shutil
from sys import platform

root = Path(__file__).parent

subprocess.run([
    'git', 'submodule', 'update', '--init', '--recursive',
], cwd=root)

def get_profiles_ini():
    if platform == 'win32':
        return Path(os.environ['APPDATA'])/'Mozilla'/'Firefox'/'profiles.ini'
    elif platform == 'darwin':
        return Path('~/Library/Application Support/Firefox/profiles.ini').expanduser()
    else:
        return Path('~/.mozilla/firefox/profiles.ini').expanduser()

profiles_ini = get_profiles_ini()

config = configparser.ConfigParser()
config.read(profiles_ini)

for section in config.sections():
    if not section.startswith('Profile'):
        continue

    name = config.get(section, 'Name')
    if config.getboolean(section, 'IsRelative', fallback=True):
        profile_path = profiles_ini.parent / config.get(section, 'Path')
    else:
        profile_path = Path(config.get(section, 'Path'))

    print(f'Installing to {name} ({profile_path})')
    shutil.rmtree(profile_path / 'chrome', ignore_errors=True)
    shutil.copytree(
        src=str(root / 'chrome') + '/',
        dst=str(profile_path / 'chrome'),
    )
