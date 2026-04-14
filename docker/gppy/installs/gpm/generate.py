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
        self._trax: List[str] = []
        self._hitrax: List[str] = []
        self._stdtrax: List[str] = []
        self._fpart: Path = Path("/")

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
        for value in (
            self._session.query(Track.album, Track.date)
            .distinct()
            .where(Track.artist == artist)
            .order_by(Track.date)
        ):
            albums.append(value[0])
        print(f"* {artist}")
        if len(albums) > 1:
            self._trax = []
            self._hitrax = []
            self._stdtrax = []
            for item in albums:
                # print(f"\t {item}")
                self._get_trax(artist, item)
            fpath: Path = self._target.joinpath(self._fpart, f"{artist} (All).m3u")
            hipath: Path = self._target.joinpath(self._fpart, f"{artist} (Hires).m3u")
            stdpath: Path = self._target.joinpath(self._fpart, f"{artist} (Std).m3u")
            print(f"\t{str(fpath)}", flush=True)
            with open(fpath, "w", encoding="utf8") as fyle:
                for nitem in self._trax:
                    fyle.write(nitem)
                    fyle.write("\n")
            fyle.close()
            if len(self._stdtrax) > 0:
                print(f"\t{str(stdpath)}", flush=True)
                with open(stdpath, "w", encoding="utf8") as fylestd:
                    for nitem in self._stdtrax:
                        fylestd.write(nitem)
                        fylestd.write("\n")
                    fylestd.close()
            if len(self._hitrax) > 0:
                print(f"\t{str(hipath)}", flush=True)
                with open(hipath, "w", encoding="utf8") as fylehi:
                    for nitem in self._hitrax:
                        fylehi.write(nitem)
                        fylehi.write("\n")
                    fylehi.close()

    def _get_trax(self, artist: str, album: str):
        for value in (
            self._session.query(
                Track.file, Track.title, Track.length, Track.path, Track.hires
            )
            .where(Track.artist == artist, Track.album == album)
            .order_by(Track.file)
        ):
            tpath: Path = Path(value[3])
            subpath: Path = Path(tpath.parts[1], tpath.parts[2])
            self._fpart: Path = Path(tpath.parts[0])
            m3ustr = f"#EXTINF:{value[2]},{artist} - {value[1]}"
            self._trax.append(m3ustr)
            self._trax.append(str(subpath))
            if value[4] == 1:
                self._hitrax.append(m3ustr)
                self._hitrax.append(str(subpath))
            else:
                self._stdtrax.append(m3ustr)
                self._stdtrax.append(str(subpath))
