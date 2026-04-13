import json
from typing import List
from pathlib import Path

from .db import Database, Track


class Generator:

    def __init__(self, target: Path, source: Database):
        """Run here"""
        self._artists: str = []
        self._albums = []
        self._source: Database = source
        self._session = self._source.session
        self._target: Path = target

        self._get_artists()

    def _get_artists(self):
        for value in self._session.query(Track.artist).distinct():
            self._artists.append(value[0])
        self._artists.sort()
        # print(self._artists)
        for art in self._artists:
            self._get_artist_albums(art)

    def _get_artist_albums(self, artist: str):
        albums = []
        for value in self._session.query(Track.album, Track.date).distinct().where(Track.artist==artist).order_by(Track.date):
            self._albums.append(value[0])
        print(f"* {artist}")
        if len(albums) > 2:
            self._trax = []
            fpath: Path = self._target.joinpath(artist,f"{artist}.m3u")
            for item in albums:
                # print(f"\t {item}")
                self._get_trax(artist, item)
            with open(fpath,"w",encoding="utf8") as fyle:
                for nitem in self._trax:
                    fyle.write(nitem)
                    fyle.write("\n|")
            fyle.close()
    
    def _get_trax(self, artist: str, album: str):
        for value in self._session.query(Track.file, Track.title, Track.length, Track.path).where(Track.artist==artist, Track.album==album).order_by(Track.file):
            tpath: Path = Path(value[3])
            subpath: Path = Path(tpath.parts[1], tpath.parts[2])
            m3ustr = f"#EXTINF:{value[2]},{artist} - {value[1]}"
            self._trax.append(m3ustr)
            self._trax.append(subpath)
        
