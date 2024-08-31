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
import requests
from datetime import datetime
from time import sleep
from tqdm import tqdm


BASE_BEATMAPSET_URL = 'https://osu.ppy.sh/beatmapsets'
BASE_BEATMAPSET_FOLDER = pathlib.Path(f'{os.getenv("HOME")}/www/beatmaps')


def download_beatmap(beatmapset: ossapi.BeatmapsetCompact, osu_session: str):
    beatmapset_filename = f"{beatmapset.id} {beatmapset.artist} - {beatmapset.title}.osz"
    beatmapset_ranked_date = beatmapset.expand().ranked_date
    download_folder = BASE_BEATMAPSET_FOLDER / str(beatmapset_ranked_date.year) / str(beatmapset_ranked_date.month)

    if not download_folder.exists():
        download_folder.mkdir(0o755, parents=True)

    if (download_folder / beatmapset_filename).exists():
        print(f'"{beatmapset_filename}" already downloaded')
        return

    with requests.sessions.Session() as s:
        s.cookies.set('osu_session', osu_session)
        s.headers = {
            'Referer': f'https://osu.ppy.sh/beatmapsets/{beatmapset.id}'
        }
        s.stream = True
        r = s.get(f'https://osu.ppy.sh/beatmapsets/{beatmapset.id}/download')
        total = int(r.headers.get('content-length', 0))
        with open(download_folder / beatmapset_filename, "wb") as f, tqdm(
            desc=beatmapset_filename,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in r.iter_content(chunk_size=1024):
                size = f.write(data)
                bar.update(size)


def count_beatmaps(client_id, client_secret):
    months = [0, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    api = ossapi.Ossapi(client_id, client_secret)

    current_year = datetime.now().year
    for year in range(2007, current_year+1):
        for month in range(1, 13):
            total = 0

            if year == 2007 and month < 10:
                continue

            if year == current_year and month > datetime.now().month:
                continue

            query = f'ranked>={year}-{month}-01 '
            if month == 12:
                query += f'ranked<{year+1}-01-01'
            else:
                query += f'ranked<{year}-{month+1}-01'

            beatmapsets = api.search_beatmapsets(query, explicit_content=ossapi.BeatmapsetSearchExplicitContent.SHOW)
            total += beatmapsets.total
            cursor = beatmapsets.cursor
            while cursor is not None:
                beatmapsets = api.search_beatmapsets(query, cursor=cursor)
                total += beatmapsets.total
                cursor = beatmapsets.cursor

            print(f'Total beatmapsets from {months[month]} {year}:\t{total} "{query}"')
            sleep(1)
