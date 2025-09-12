import json
import pandas as pd
from fastapi.responses import StreamingResponse
from datetime import datetime
import io

from fastapi import FastAPI, Depends, UploadFile, Body, File, HTTPException, Form
from sqlalchemy.orm import Session

from clean import clean_north, clean_south, clean_west, clean_east
from data_model import MapInput, parse_map, Action
from db import get_db, Map, post_session, CleaningSession

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
    status = None
    cleaned_tiles = []
    start_time = datetime.now()
    map = db.query(Map).filter(Map.id == id).first()
    num_of_actions = 0
    try:
        if not map:
            raise HTTPException(status_code=404, detail="Map not found")
        elif map.data['rows'] < x or map.data['cols'] < y:
            raise HTTPException(status_code=400, detail="Un-correct starting point")
        else:
            map_data = map.data
            tiles = map_data['tiles']
            start_point = (x, y)
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
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        map_id = map.id
        num_cleaned_tiles = len(cleaned_tiles)

        post_session(
            map_id=map_id,
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


@app.get("/history/")
def history(map_id: str, db: Session = Depends(get_db)):
    try:
        sessions = db.query(CleaningSession).filter(CleaningSession.map_id == map_id).all()

        if not sessions:
            raise HTTPException(status_code=404, detail="No sessions found for this map")

        # Converti in lista di dizionari
        data = [
            {
                "id": s.id,
                "map_id": s.map_id,
                "start_time": s.start_time,
                "final_state": s.final_state,
                "number_of_actions": s.number_of_actions,
                "number_of_cleaned_tiles": s.number_of_cleaned_tiles,
                "duration": s.duration
            }
            for s in sessions
        ]

        df = pd.DataFrame(data)
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        stream.seek(0)

        return StreamingResponse(
            stream,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=history_map_{map_id}.csv"}
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/extended-functionality/")
def extended_functionality(nome: str, email: str, db: Session = Depends(get_db)):
    pass
