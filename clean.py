from datetime import datetime
from fastapi import HTTPException
from db import Map, post_session


def cleaning_session(id: int, x: int, y: int, actions: list, db):
    status = None
    cleaned_tiles = []
    start_time = datetime.now()
    num_of_actions = 0

    map_obj = db.query(Map).filter(Map.id == id).first()

    if not map_obj:
        raise HTTPException(status_code=404, detail="Map not found")
    elif map_obj.data['rows'] < x or map_obj.data['cols'] < y:
        raise HTTPException(status_code=400, detail="Un-correct starting point")

    map_data = map_obj.data
    tiles = map_data['tiles']
    start_point = (x, y)

    try:
        for num_of_actions, action in enumerate(actions):
            step = action.step
            if action.direction == 'north':
                ct, status = clean_north(start_point, step, tiles)
            elif action.direction == 'south':
                ct, status = clean_south(start_point, step, tiles)
            elif action.direction == 'west':
                ct, status = clean_west(start_point, step, tiles)
            else:
                ct, status = clean_east(start_point, step, tiles)

            cleaned_tiles.extend(ct)

            if status != 'success':
                raise HTTPException(status_code=400, detail=status)
    except Exception as e:
        status = 'failure'
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        num_cleaned_tiles = len(cleaned_tiles)

        if map_obj:
            post_session(
                map_id=map_obj.id,
                start_time=start_time,
                final_state=status,
                number_of_actions=num_of_actions,
                num_cleaned_tiles=num_cleaned_tiles,
                duration=duration,
                db=db
            )

        report = {
            'cleaned_tiles': cleaned_tiles,
            'status': status
        }
        return report


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
