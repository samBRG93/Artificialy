from fastapi import HTTPException


def clean_north(start_point, step, tiles):
    cleaned_tiles = []
    try:
        for s in range(1, step + 1):
            y_target_tile = start_point[1] - s
            x_target_tile = start_point[0]

            selected_tile = next(
                (tile for tile in tiles if tile['x'] == x_target_tile and tile['y'] == y_target_tile),
                None
            )
            if not selected_tile:
                raise HTTPException(status_code=404, detail="Tile not found")

            if not selected_tile['walkable']:
                raise HTTPException(status_code=400, detail="Step not walkable")
            else:
                print('Salvare Sessione')
                cleaned_tiles.append(selected_tile)

        return cleaned_tiles, 'success'
    except Exception:
        return cleaned_tiles, 'failure'


def clean_south(start_point, step, tiles):
    cleaned_tiles = []
    try:
        for s in range(1, step + 1):
            y_target_tile = start_point[1] + s
            x_target_tile = start_point[0]

            selected_tile = next(
                (tile for tile in tiles if tile['x'] == x_target_tile and tile['y'] == y_target_tile),
                None
            )
            if not selected_tile:
                raise HTTPException(status_code=404, detail="Tile not found")

            if not selected_tile['walkable']:
                raise HTTPException(status_code=400, detail="Step not walkable")
            else:
                print('Salvare Sessione')
                cleaned_tiles.append(selected_tile)

        return cleaned_tiles, 'success'
    except Exception:
        return cleaned_tiles, 'failure'


def clean_east(start_point, step, tiles):
    cleaned_tiles = []
    try:
        for s in range(1, step + 1):
            x_target_tile = start_point[0] + s
            y_target_tile = start_point[1]

            selected_tile = next(
                (tile for tile in tiles if tile['x'] == x_target_tile and tile['y'] == y_target_tile),
                None
            )
            if not selected_tile:
                raise HTTPException(status_code=404, detail="Tile not found")

            if not selected_tile['walkable']:
                raise HTTPException(status_code=400, detail="Step not walkable")
            else:
                print('Salvare Sessione')
                cleaned_tiles.append(selected_tile)

        return cleaned_tiles, 'success'
    except Exception:
        return cleaned_tiles, 'failure'


def clean_west(start_point, step, tiles):
    cleaned_tiles = []
    try:
        for s in range(1, step + 1):
            x_target_tile = start_point[0] - s
            y_target_tile = start_point[1]

            selected_tile = next(
                (tile for tile in tiles if tile['x'] == x_target_tile and tile['y'] == y_target_tile),
                None
            )
            if not selected_tile:
                raise HTTPException(status_code=404, detail="Tile not found")

            if not selected_tile['walkable']:
                raise HTTPException(status_code=400, detail="Step not walkable")
            else:
                print('Salvare Sessione')
                cleaned_tiles.append(selected_tile)

        return cleaned_tiles, 'success'
    except Exception:
        return cleaned_tiles, 'failure'
