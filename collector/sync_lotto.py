from datetime import datetime
from sqlalchemy import delete

from app.db import SessionLocal, settings
from app.models import LottoDraw
from collector.client import fetch_draws, LottoFetchError


def to_model(row: dict) -> LottoDraw:
    draw_date = datetime.strptime(row["ltRflYmd"], "%Y%m%d").date()

    return LottoDraw(
        draw_no=row["ltEpsd"],
        draw_date=draw_date,
        n1=row["tm1WnNo"],
        n2=row["tm2WnNo"],
        n3=row["tm3WnNo"],
        n4=row["tm4WnNo"],
        n5=row["tm5WnNo"],
        n6=row["tm6WnNo"],
        bonus=row["bnsWnNo"],
    )


def sync_range(start_draw_no: int, end_draw_no: int):
    if start_draw_no < 1:
        raise ValueError("시작 회차는 1 이상이어야 합니다.")

    if end_draw_no < start_draw_no:
        raise ValueError("종료 회차는 시작 회차보다 크거나 같아야 합니다.")

    db = SessionLocal()
    try:
        rows = fetch_draws(start_draw_no, end_draw_no)

        if not rows:
            raise LottoFetchError("가져온 데이터가 비어 있습니다.")

        rows = sorted(rows, key=lambda x: x["ltEpsd"])
        models = [to_model(row) for row in rows]

        db.execute(
            delete(LottoDraw).where(
                LottoDraw.draw_no >= start_draw_no,
                LottoDraw.draw_no <= end_draw_no,
            )
        )

        db.add_all(models)
        db.commit()

        print(f"[DONE] synced rows={len(models)}")
        print(f"[INFO] start={models[0].draw_no}, end={models[-1].draw_no}")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main():
    sync_range(
        start_draw_no=settings.LOTTO_START_DRAW_NO,
        end_draw_no=settings.LOTTO_END_DRAW_NO,
    )


if __name__ == "__main__":
    main()