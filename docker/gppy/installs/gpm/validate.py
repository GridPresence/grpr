import json
from typing import Dict, Any
from pathlib import Path

from .audio import AUDIO_FORMATS as AFORMATS
from .audio import LibFile, FlacFile

LIMIT = 1000


class Validator:

    def __init__(self, source: Path):
        """Run here"""
        ctr = 0
        outrctr = 0
        for fyle in self._walk(spath=source):
            if fyle.suffix in AFORMATS:
                # print(json.dumps(self.tags(fyle, source), indent=4,sort_keys=True))
                try:
                    tval = self.tags(fyle, source, validate=True)
                except KeyError:
                    pass

    def _flac_tags(self, spath: Path, root: Path, validate: bool) -> Dict[str, str]:
        """Return the tags from a FLAC file"""
        libf = LibFile(spath, root)
        flak = FlacFile(libf, validate)
        return flak.tags

    def _mp3_tags(self, spath: Path, root: Path) -> Dict[str, str]:
        """Return the ID3 tags from an MP3 file"""
        retval: Dict[str, str] = {}
        mpthree = MP3(spath)
        idthree = ID3(spath)
        # print(idthree.pprint())
        retval["length"] = int(mpthree.info.length)
        retval["artist"] = idthree["TPE1"].text[0]
        retval["disc"] = idthree["TPOS"].text[0]
        retval["track"] = idthree["TRCK"].text[0]
        try:
            retval["date"] = idthree["TDRC"].text[0]
        except KeyError:
            print(idthree.pprint())
            retval["date"] = "1962-12-22"
        retval["album"] = idthree["TALB"].text[0]
        retval["title"] = idthree["TIT2"].text[0]
        retval["genre"] = idthree["TCON"].text[0]
        try:
            retval["composer"] = idthree["TCOM"].text[0]
        except KeyError:
            retval["composer"] = "Unknown"
        return retval

    def tags(self, spath: Path, root: Path, validate: bool = False) -> Dict[str, str]:
        """Extract relevant tags according to format"""
        if spath.suffix == ".flac":
            return self._flac_tags(spath, root, validate)
        return self._mp3_tags(spath, root)

    def _walk(self, spath: Path):
        """Some stuff"""
        for path in sorted(spath.iterdir(), reverse=False):
            if path.is_dir():
                # print(path)
                yield from self._walk(path)
                continue
            yield path.resolve()
