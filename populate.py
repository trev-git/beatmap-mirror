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
from dotenv import dotenv_values
from download import download_beatmap
from time import sleep


def main():
    config = dotenv_values('.env')
    api = ossapi.Ossapi(config['CLIENT_ID'], config['CLIENT_SECRET'])

    for i in range(2007, 2025):
        beatmapsets = api.search_beatmapsets(f'ranked={i}')
        for bms in beatmapsets.beatmapsets:
            beatmapset = api.beatmapset(bms.id)
            download_beatmap(beatmapset, config['OSU_SESSION_COOKIES'])
            sleep(2)


if __name__ == '__main__':
    main()
