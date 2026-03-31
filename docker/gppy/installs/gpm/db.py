from sqlalchemy import create_engine, URL, MetaData
from sqlalchemy import Table, Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


# class Artist(Base):
#     __tablename__ = "artists"

#     id: Mapped[str] = mapped_column(primary_key=True)


#     def __init__(self):
#         pass


class Album(Base):
    __tablename__ = "albums"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


#     def __init__(self):
#         pass


class Database:
    def __init__(self):
        self._url = URL.create(
            "mysql+mysqlconnector",
            username=os.getenv("MyUser"),
            password=os.getenv("MyPassword"),
            host=os.getenv("MyServer"),
            database=os.getenv("MyDb"),
        )
        self._engine = create_engine(
            self._url, echo=True, insertmanyvalues_page_size=100
        )
        Base.metadata.create_all(self._engine)
        self._session = Session(self._engine)

    def __del__(self):
        self._session.commit()

    def insert(self, fyle: FlacFile):
        iTrack = Track(fyle)
        self._session.add(iTrack)


class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    artist: str = Column(String(128), nullable=False)
    album: str = Column(String(128), nullable=False)
    bps: int = Column(Integer(), nullable=False)
    channels: int = Column(Integer(), nullable=False)
    length: int = Column(Integer(), nullable=False)
    rate: int = Column(Integer(), nullable=False)
    size: int = Column(Integer(), nullable=False)
    date: str = Column(String(4), nullable=False)
    disc: str = Column(String(2), nullable=False)
    disc_total: str = Column(String(2), nullable=False)
    track: str = Column(String(2), nullable=False)
    track_total: str = Column(String(2), nullable=False)
    title: str = Column(String(128), nullable=False)
    file: str = Column(String(128), nullable=False)
    path: str = Column(String(255), nullable=False)
    genre: str = Column(String(32), nullable=False)
    hires: bool = Column(Boolean(), default=False)
    valid: bool = Column(Boolean(), default=False)

    def __init__(self, trk: FlacFile):
        self.artist = trk.artist
        self.album = trk.album
        self.bps = trk.bits_per_sample
        self.channels = trk.channels
        self.length = trk.length
        self.rate = trk.sample_rate
        self.size = trk.size
        self.date = trk.data
        self.disc = trk.discnumber
        self.disc_total = trk.disctotal
        self.track = trk.tracknumber
        self.track_total = trk.tracktotal
        self.title = trk.title
        self.file = trk.file
        self.path = trk.path
        self.genre = trk.genre
        self.hires = trk.hires
        self.valid = trk.valid
