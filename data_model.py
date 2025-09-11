from pydantic import BaseModel, field_validator
from typing import List


class Tile(BaseModel):
    x: int
    y: int
    walkable: bool

    @field_validator("walkable")
    def check_tiles(cls, walkable):
        if walkable != 'O' and walkable != 'X':
            raise ValueError("walkable must be either 'O' or 'X'")


class MapInput(BaseModel):
    rows: int
    cols: int
    tiles: List[Tile]

    @field_validator("cols")
    def check_square(cls, v, values):
        if "rows" in values and values["rows"] != v:
            raise ValueError("Map must be squared")
        return v

    @field_validator("tiles")
    def check_tiles(cls, tiles):
        if len(tiles) < 2:
            raise ValueError("Map must be walkable")
