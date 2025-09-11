from fastapi import FastAPI, Depends, UploadFile, Body, File
from sqlalchemy.orm import Session

from data_model import MapInput
from db import get_db, Map

# --- FastAPI ---
app = FastAPI()


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
        "columns": cols,
        "tiles": []
    }
    for y, line in enumerate(lines):
        for x, char in enumerate(line):

            if char != 'O' and char != 'X':
                raise ValueError('Map cells must be O or X')
            data['tiles'].append(
                {"x": x, "y": y, "walkable": True if char == "O" else False}
            )

    return data


@app.post("/set-map/")
def set_map(id: int,
            json_data: MapInput | None = Body(default=None),
            file: UploadFile | None = File(default=None),
            db: Session = Depends(get_db)):
    if json_data:
        data = json_data.dict()
    elif file:
        content = file.read().__str__()
        data = parse_map(content)
    else:
        raise ValueError(f"Format {format} not supported")

    map = Map(id=id, data=data)
    db.add(map)
    db.commit()
    db.refresh(map)
    return map


# Rotta: aggiungi utente
@app.post("/clean/")
def clean(nome: str, email: str, db: Session = Depends(get_db)):
    user = User(nome=nome, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/history/")
def clean(nome: str, email: str, db: Session = Depends(get_db)):
    user = User(nome=nome, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/extended-functionality/")
def clean(nome: str, email: str, db: Session = Depends(get_db)):
    user = User(nome=nome, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
