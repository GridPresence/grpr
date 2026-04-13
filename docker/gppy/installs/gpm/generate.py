import json
from typing import Dict, Any
from pathlib import Path

from .db import Database, Track


class Generator:

    def __init__(self, target: Path, source: Database):
        """Run here"""
        self._artists: str = []
        self._albums = []
        self._source: Database = source
        self._session = self._source.session

        self._get_artists()

    def _get_artists(self):
        for value in self._session.query(Track.artist).distinct():
            self._artists.append(value[0])
        print(self._artists)
        for art in self._artists:
            self._get_artist_albums(art)

    def _get_artist_albums(self, artist: str):
        self._albums = []
        for value in self._session.query(Track.album).distinct().where(Track.artist==artist):
            self._albums.append(value[0])
        print(f"----- {artist}")
        print(self._albums)
