import json
from typing import Dict, Any
from pathlib import Path

from .db import Database, Track


class Generator:

    def __init__(self, target: Path, source: Database):
        """Run here"""
        self._artists: str = []
        self._source: Database = source
        self._session = self._source.session

        self._get_artists()

    def _get_artists(self):
        self._artists = self._session.query(Track.artist)
        print(self._artists)
