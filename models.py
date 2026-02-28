from sqlmodel import SQLModel, Field, create_engine
from typing import Optional

class Bio(SQLModel, table=True):
    first_name: str = Field(primary_key = True)
    last_name: str = Field(primary_key = True)
    number: int | None = None
    position: str | None = None
    height: str | None = None
    weight: int | None = None
    academic_class: str | None = None
    hometown: str | None = None
    high_school: str | None = None

class Stats(SQLModel, table=True):
    first_name: str = Field(primary_key=True, foreign_key="bio.first_name")
    last_name: str = Field(primary_key=True, foreign_key="bio.last_name")
    number: Optional[str] = None
    GP: Optional[int] = None
    G: Optional[int] = None
    A: Optional[int] = None
    PTS: Optional[int] = None
    SH: Optional[int] = None
    SH_PCT: Optional[float] = None
    Plus_Minus: Optional[int] = None
    PPG: Optional[int] = None
    SHG: Optional[int] = None
    FG: Optional[int] = None
    GWG: Optional[int] = None
    GTG: Optional[int] = None
    OTG: Optional[int] = None
    HTG: Optional[int] = None
    UAG: Optional[int] = None
    PN_PIM: Optional[str] = None
    MIN: Optional[int] = None
    MAJ: Optional[int] = None
    OTH: Optional[int] = None
    BLK: Optional[int] = None

engine = create_engine('sqlite:///hockey.db')
SQLModel.metadata.create_all(engine)