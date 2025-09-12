import json
import os
import pandas as pd
from fastapi.responses import StreamingResponse
from datetime import datetime, timedelta
import io
from fastapi import FastAPI, Depends, UploadFile, Body, File, HTTPException, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from starlette import status
from data_model import MapInput, parse_map, Action
from db import get_db, Map, CleaningSession
from clean import execute_cleaning_session
from passlib.context import CryptContext
import dotenv

app = FastAPI()
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
dotenv.load_dotenv()

USERS = {
    "admin": os.getenv("ADMIN_USER_HASH"),
}


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    os.getenv('users')
    hashed = USERS.get(credentials.username)
    if not hashed or not pwd_context.verify(credentials.password, hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.post("/set-map/")
async def set_map(
        id: int, json_data: str | None = Form(default=None), file: UploadFile | None = File(default=None),
        db: Session = Depends(get_db), _user: str = Depends(get_current_user)):
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
def clean(id: int, x: int, y: int, actions: list[Action] = Body(...), db: Session = Depends(get_db),
          _user: str = Depends(get_current_user)):
    return execute_cleaning_session(id, x, y, actions, db)


@app.get("/history/")
def history(map_id: str, db: Session = Depends(get_db), _user: str = Depends(get_current_user)):
    try:
        sessions = db.query(CleaningSession).filter(CleaningSession.map_id == map_id).all()

        if not sessions:
            raise HTTPException(status_code=404, detail="No sessions found for this map")

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


@app.post("/extended-functionality/")
def extended_functionality(id: int, x: int, y: int, actions: list[Action] = Body(...), db: Session = Depends(get_db),
                           _user: str = Depends(get_current_user)):
    session = db.query(CleaningSession).filter(CleaningSession.map_id == id).order_by(
        CleaningSession.start_time.desc()).first()

    if session:
        end_time = session.start_time + timedelta(seconds=session.duration)
        if end_time >= datetime.now() - timedelta(days=1):
            return {
                "id": id,
                "message": f"Map with id: {id} has been cleaned in date: {end_time}. No need for cleaning"
            }
    else:
        return execute_cleaning_session(id, x, y, actions, db)
