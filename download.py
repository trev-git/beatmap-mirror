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


BASE_BEATMAPSET_URL = 'https://osu.ppy.sh/beatmapsets'
BASE_BEATMAPSET_FOLDER = pathlib.Path(f'{os.getenv("HOME")}/www/beatmaps')


def download_beatmap(beatmapset: ossapi.Beatmapset, osu_session: str):
    beatmap_filename = f"{beatmapset.id} {beatmapset.artist} - {beatmapset.title}.osz"
    download_folder = BASE_BEATMAPSET_FOLDER / str(beatmapset.ranked_date.year)

    print(f'Starting download of "{beatmap_filename}"')

    if not download_folder.exists():
        download_folder.mkdir(0o755)

    if (download_folder / beatmap_filename).exists():
        print(f'"{beatmap_filename}" already downloaded')
        return

    with requests.sessions.Session() as s:
        s.cookies.set('osu_session', osu_session)
        s.headers = {
            'Referer': f'https://osu.ppy.sh/beatmapsets/{beatmapset.id}'
        }
        r = s.get(f'https://osu.ppy.sh/beatmapsets/{beatmapset.id}/download')
        with open(download_folder / beatmap_filename, "wb") as f:
            f.write(r.content)

    print(f'Finished downloading "{beatmap_filename}"')
