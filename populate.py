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
from datetime import datetime
from dotenv import dotenv_values
from download import download_beatmap
from time import sleep


def main():
    months = [0, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    config = dotenv_values('.env')
    api = ossapi.Ossapi(config['CLIENT_ID'], config['CLIENT_SECRET'])

    current_year = datetime.now().year
    for year in range(2007, current_year+1):
        for month in range(1, 13):
            if year == 2007 and month < 10:
                continue

            if year == current_year and month > datetime.now().month:
                continue

            print(f'Downloading maps from {months[month]} {year}')
            query = f'ranked>{year}-{month}-01 '
            if month == 12:
                query += f'ranked<{year+1}-01-01'
            else:
                query += f'ranked<{year}-{month+1}-01'

            beatmapsets = api.search_beatmapsets(f'ranked<{year}-{month}-01')
            for bms in beatmapsets.beatmapsets:
                beatmapset = api.beatmapset(bms.id)
                download_beatmap(beatmapset, config['OSU_SESSION_COOKIES'])
                sleep(2)


if __name__ == '__main__':
    main()
