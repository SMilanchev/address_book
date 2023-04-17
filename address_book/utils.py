from sqlalchemy.orm import Session


def filter_step_by_step(db: Session, model, filter_params: dict) -> []:
    stmt = db.query(model)
    for attr, val in filter_params.items():
        stmt = stmt.filter(getattr(model, attr) == val)
    return stmt.all()
