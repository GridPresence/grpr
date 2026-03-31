from typing import Dict, Any
from pathlib import Path

from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.flac import FLAC, StreamInfo

AUDIO_FORMATS = [".mp3", ".flac"]
PLAYLIST_FORMATS = [".m3u"]


class LibFile:
    """
    A description of a library file
    """

    def __init__(self, src: Path, root: Path):
        self._fullpath: Path = src.resolve()
        self._path: Path = self._fullpath.relative_to(root)
        self._modified: int = 0
        self._exists: bool = False
        self._size: int = 0
        self.refresh_state()

    def __str__(self) -> str:
        return f"{self._path}: ({self._modified} ... {self._size})"

    @property
    def name(self) -> str:
        """Accessor"""
        return self._path.name

    @property
    def parent(self) -> Path:
        """Accessor"""
        return self._path.parent

    @property
    def path(self) -> Path:
        """Accessor"""
        return self._path

    @property
    def fullpath(self) -> Path:
        """Accessor"""
        return self._fullpath

    @property
    def suffix(self) -> str:
        """Accessor"""
        return self._fullpath.suffix

    @property
    def exists(self) -> bool:
        """Accessor"""
        return self._exists

    @property
    def modified(self) -> int:
        """Accessor"""
        return self._modified

    @property
    def size(self) -> int:
        """Accessor"""
        return self._size

    def refresh_state(self):
        """
        Update knowledge about the file state
        """
        self._exists = self._fullpath.exists()
        if self._exists:
            self._modified = int(self._fullpath.stat().st_mtime)
            self._size = self._fullpath.stat().st_size


class FlacFile:
    """Wrapper class"""

    def __init__(self, sbj: LibFile):
        self._sbj: LibFile = sbj
        self._mdata: Dict[str, Any] = {}
        self._mdata["path"] = str(self._sbj.path)
        self._mdata["file"] = self._sbj.path.name
        self._mdata["valid"] = False
        self._mdata["hires"] = False
        if (self._sbj.exists) and (self._sbj.suffix == ".flac"):
            self._mdata["valid"] = True
        if self._mdata["valid"]:
            self._mdata["size"] = self._sbj.size
            self._flac: FLAC = FLAC(self._sbj.fullpath)
            _info: StreamInfo = self._flac.info
            self._mdata["sample_rate"] = _info.sample_rate
            self._mdata["bits_per_sample"] = _info.bits_per_sample
            self._mdata["channels"] = _info.channels
            self._mdata["bitrate"] = _info.bitrate
            self._mdata["length"] = (int)(_info.length + 1)
            if (self._mdata["bits_per_sample"] > 16) or (
                self._mdata["sample_rate"] > 44100
            ):
                self._mdata["hires"] = True
            for k, v in self._flac.tags:
                self._mdata[k] = v
            print(self._mdata)

    def __getitem__(self, key):
        return self._mdata[key]

    # @property
    # def valid(self):
    #     """Accessor"""
    #     return self._mdata["valid"]

    # @property
    # def artist(self):
    #     """Accessor"""
    #     return self._mdata["artist"]

    # @property
    # def album(self):
    #     """Accessor"""
    #     return self._mdata["album"]

    # @property
    # def tags(self):
    #     """Accessor"""
    #     return self._mdata

    # @property
    # def sample_rate(self) -> int:
    #     """Accessor"""
    #     if self.valid:
    #         return self._mdata["sample_rate"]
    #     return -1

    # @property
    # def bits_per_sample(self) -> int:
    #     """Accessor"""
    #     if self.valid:
    #         return self._mdata["bits_per_sample"]
    #     return -1

    # @property
    # def channels(self) -> int:
    #     """Accessor"""
    #     if self.valid:
    #         return self._mdata["channels"]
    #     return -1

    # @property
    # def bitrate(self) -> int:
    #     """Accessor"""
    #     if self.valid:
    #         return self._mdata["bitrate"]
    #     return -1

    # @property
    # def hires(self) -> bool:
    #     """Accessor"""
    #     if self.valid:
    #         return self._mdata["hires"]
    #     return False

    # @property
    # def genre(self) -> str:
    #     """Accessor"""
    #     if self.valid:
    #         return self._mdata["genre"]
    #     return "NULL"

    def __str__(self) -> str:
        tstr = json.dumps(self._mdata, indent=4, sort_keys=True)
        return tstr
