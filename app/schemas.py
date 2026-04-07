from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class LottoDrawCreate(BaseModel):
    draw_no: int
    draw_date: date
    n1: int
    n2: int
    n3: int
    n4: int
    n5: int
    n6: int
    bonus: int


class LottoDrawResponse(BaseModel):
    id: int
    draw_no: int
    draw_date: date
    n1: int
    n2: int
    n3: int
    n4: int
    n5: int
    n6: int
    bonus: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)