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
from time import sleep
from beatmaps import download_beatmap


def main():
    config = dotenv_values('.env')
    api = ossapi.Ossapi(config['CLIENT_ID'], config['CLIENT_SECRET'])

    events = api.beatmapset_events(limit=10, page=1, user_id=None, types=[ossapi.BeatmapsetEventType.RANK])
    for event in events.events:
        download_beatmap(event.beatmapset, config['OSU_SESSION_COOKIES'])
        sleep(5)


if __name__ == '__main__':
    main()
