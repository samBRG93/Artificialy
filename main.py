import json

from fastapi import FastAPI, Depends, UploadFile, Body, File, HTTPException, Form
from sqlalchemy.orm import Session

from data_model import MapInput, parse_map
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
def clean(nome: str, email: str, db: Session = Depends(get_db)):
    pass


@app.get("/history/")
def clean(nome: str, email: str, db: Session = Depends(get_db)):
    pass


@app.get("/extended-functionality/")
def clean(nome: str, email: str, db: Session = Depends(get_db)):
    pass
