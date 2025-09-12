import json
import time

from fastapi import FastAPI, Depends, UploadFile, Body, File, HTTPException, Form
from sqlalchemy.orm import Session

from clean import clean_north, clean_south, clean_west, clean_east
from data_model import MapInput, parse_map, Action
from db import get_db, Map

app = FastAPI()


@app.post("/set-map/")
async def set_map(id: int,
                  json_data: str | None = Form(default=None),
                  file: UploadFile | None = File(default=None),
                  db: Session = Depends(get_db)):
    try:
        if json_data:
            parsed = json.loads(json_data)

            validated = MapInput(**parsed)
            data = validated.dict()
        elif file:
            content = await file.read()
            text = content.decode("utf-8")

            parsed = parse_map(text)
            validated = MapInput(**parsed)
            data = validated.dict()

        else:
            raise ValueError(f"Format {format} not supported")

        map = db.query(Map).filter(Map.id == id).first()

        if map:
            map.data = data
        else:
            map = Map(id=id, data=data)
            db.add(map)

        db.commit()
        db.refresh(map)
        return map
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Rotta: aggiungi utente
@app.post("/clean/")
def clean(id: int, x: int, y: int, actions: list[Action] = Body(...), db: Session = Depends(get_db)):
    map = db.query(Map).filter(Map.id == id).first()

    if not map:
        raise HTTPException(status_code=404, detail="Map not found")
    elif map.data['rows'] < x or map.data['cols'] < y:
        raise HTTPException(status_code=400, detail="Un-correct starting point")
    else:
        cleaned_tiles = []
        map_data = map.data
        tiles = map_data['tiles']
        start_point = (x, y)
        for action in actions:
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

            if status is not 'success':
                #todo: insert db session
                return {
                    'cleaned_tiles': cleaned_tiles,
                    'status': status
                }

        # todo: insert db session
        return {
            'cleaned_tiles': cleaned_tiles,
            'status': 'success'
        }


@app.get("/history/")
def history(nome: str, email: str, db: Session = Depends(get_db)):
    pass


@app.get("/extended-functionality/")
def extended_functionality(nome: str, email: str, db: Session = Depends(get_db)):
    pass
