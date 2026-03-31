from uuid import UUID, uuid4

from typing import Dict, Any
from pathlib import Path

from .audio import AUDIO_FORMATS as AFORMATS


class Extractor:

    def __init__(self, source: Path, target: Database):
        """Run here"""
        fast_run_ctr = 0
        for fyle in walk(spath=source):
            if fyle.suffix in AFORMATS:
                print(json.dumps(tags(fyle, source), indent=4, sort_keys=True))
                tval = tags(fyle, source)
                target.insert(tval)
            fast_run_ctr += 1
            if fast_run_ctr > 10:
                return

    def flac_tags(self, spath: Path, root: Path) -> Dict[str, str]:
        """Return the tags from a FLAC file"""
        libf = LibFile(spath, root)
        flak = FlacFile(libf)
        return flak.tags

    def mp3_tags(self, spath: Path, root: Path) -> Dict[str, str]:
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

    def tags(self, spath: Path, root: Path) -> Dict[str, str]:
        """Extract relevant tags according to format"""
        if spath.suffix == ".flac":
            return flac_tags(spath, root)
        return mp3_tags(spath, root)

    def walk(self, spath: Path):
        """Some stuff"""
        for path in sorted(spath.iterdir(), reverse=False):
            if path.is_dir():
                print(path)
                yield from walk(path)
                continue
            yield path.resolve()
