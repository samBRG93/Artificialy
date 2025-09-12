from pydantic import BaseModel, field_validator, model_validator
from typing import List


class Tile(BaseModel):
    x: int
    y: int
    walkable: bool

    # @field_validator("walkable")
    # def check_tiles(cls, walkable):
    #     if walkable != 'O' and walkable != 'X':
    #         raise ValueError("walkable must be either 'O' or 'X'")


class MapInput(BaseModel):
    rows: int
    cols: int
    tiles: List[Tile]

    @model_validator(mode="after")
    def check_square(self):
        if self.rows != self.cols:
            raise ValueError("Map must be squared")
        return self

    @field_validator("tiles")
    @classmethod
    def check_tiles(cls, tiles):
        if len(tiles) < 2:
            raise ValueError("Map must be walkable")


def parse_map(text: str):
    lines = text.strip().splitlines()
    rows = len(lines)
    cols = len(lines[0]) if len(lines) > 0 else 0

    if rows == 0 or cols == 0:
        raise ValueError('Empty map')
    if rows == 1 and cols == 1:
        raise ValueError('Non walkable map')
    if rows != cols:
        raise ValueError('Map must be squared')

    data = {
        "rows": rows,
        "cols": cols,
        "tiles": []
    }
    for y, line in enumerate(lines):
        for x, char in enumerate(line):

            if char.capitalize() != 'O' and char.capitalize() != 'X':
                raise ValueError('Map cells must be O or X')
            data['tiles'].append(
                {"x": x, "y": y, "walkable": True if char == "O" else False}
            )

    return data
