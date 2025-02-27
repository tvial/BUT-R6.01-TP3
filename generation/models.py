from typing import List, Optional

from pydantic import BaseModel, TypeAdapter


class Track(BaseModel):
    track_id: Optional[int] = None
    path: str
    artist: str
    album: str
    track_number: int
    title: str


TrackList = TypeAdapter(List[Track])
