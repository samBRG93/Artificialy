from datetime import datetime

from pydantic import BaseModel, field_validator, model_validator
from typing import List


class User(BaseModel):
    id: int
    username: str
    password: str


class Action(BaseModel):
    direction: str
    step: int

    @field_validator("step")
    def check_step(cls, step):
        if step <= 0:
            raise ValueError("Step must be positive")
        return step

    @field_validator("direction")
    def check_direction(cls, direction: str):
        if direction.lower() not in ["north", "south", "east", "west"]:
            raise ValueError("Direction must be north, south, east, west")

        return direction.lower()


class Tile(BaseModel):
    x: int
    y: int
    walkable: bool


class MapInput(BaseModel):
    rows: int
    cols: int
    tiles: List[Tile]

    @field_validator("tiles")
    @classmethod
    def check_tiles(cls, tiles):
        if len(tiles) < 2:
            raise ValueError("Map must be walkable")

        return tiles

    @model_validator(mode="after")
    def check_consistency(self):
        if self.rows != self.cols:
            raise ValueError("Map must be squared")

        expected_tiles = self.rows * self.cols
        if len(self.tiles) != expected_tiles:
            raise ValueError(
                f"Number of tiles ({len(self.tiles)}) does not match rows*cols ({expected_tiles})"
            )

        return self


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
