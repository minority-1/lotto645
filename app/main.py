from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db import Base, engine, get_db
from app.models import LottoDraw
from app.schemas import LottoDrawCreate, LottoDrawResponse

app = FastAPI(title="lotto645")

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "lotto645 backend ok"}


@app.post("/api/lotto/draws", response_model=LottoDrawResponse)
def create_draw(payload: LottoDrawCreate, db: Session = Depends(get_db)):
    exists = db.query(LottoDraw).filter(LottoDraw.draw_no == payload.draw_no).first()
    if exists:
        raise HTTPException(status_code=409, detail="이미 존재하는 회차입니다.")

    draw = LottoDraw(**payload.model_dump())
    db.add(draw)
    db.commit()
    db.refresh(draw)
    return draw


@app.get("/api/lotto/draws", response_model=list[LottoDrawResponse])
def get_draws(db: Session = Depends(get_db)):
    return db.query(LottoDraw).order_by(desc(LottoDraw.draw_no)).all()