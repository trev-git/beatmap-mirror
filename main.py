# Automatic beatmap downloader
# Copyright (C) 2024  Khokhlov Timofey

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import ossapi
import os
import pathlib
import selenium
from selenium.webdriver.common.by import By
from dotenv import dotenv_values
from time import sleep

import selenium.types
import selenium.webdriver


BASE_FOLDER = pathlib.Path(f"{os.getenv('HOME')}/www/beatmaps/")
BASE_BEATMAPSET_URL = "https://osu.ppy.sh/beatmapsets"


def download_beatmap(beatmapset: ossapi.Beatmapset, osu_session: str):
    print(f"Starting download of {beatmapset.artist} - {beatmapset.title}")

    beatmap_year = str(beatmapset.ranked_date.year)
    download_dir = BASE_FOLDER / beatmap_year
    beatmap_filename = f"{beatmapset.id} {beatmapset.artist} - {beatmapset.title}.osz".replace(":", "_")
    download_file_path = download_dir / beatmap_filename

    print(download_file_path)

    if download_file_path.exists():
        print(f"{beatmap_filename} already downloaded!")
        return

    download_url = f"https://osu.ppy.sh/beatmapsets/{beatmapset.id}/download"

    if not download_dir.exists():
        download_dir.mkdir(mode=0o755)

    options = selenium.webdriver.FirefoxOptions()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", str(download_dir))
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

    browser = selenium.webdriver.Firefox(options=options)
    browser.get("http://osu.ppy.sh/")
    browser.add_cookie({ "name": "osu_session",  "value": osu_session })
    browser.get(f"https://osu.ppy.sh/beatmapsets/{beatmapset.id}")
    browser.find_element(By.XPATH, f'//a[@href="{download_url}"]').click()

    while not download_file_path.exists():
        print(f"Waiting for download \\ {download_file_path}", end='\r')
        print(f"Waiting for download | {download_file_path}", end='\r')
        print(f"Waiting for download / {download_file_path}", end='\r')
        print(f"Waiting for download - {download_file_path}", end='\r')
        
    print(f"Finished downloading '{beatmap_filename}'")
    browser.close()

def main():
    

    config = dotenv_values('.env')
    api = ossapi.Ossapi(config['CLIENT_ID'], config['CLIENT_SECRET'])

    events = api.beatmapset_events(limit=10, page=1, user_id=None, types=[ossapi.BeatmapsetEventType.RANK])
    for event in events.events:
        beatmapset = api.beatmapset(event.beatmapset.id)
        download_beatmap(beatmapset, config['OSU_SESSION_COOKIES'])
        sleep(2)
    



if __name__ == '__main__':
    main()
