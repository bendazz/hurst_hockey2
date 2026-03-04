from sqlmodel import Session, select
from models import engine,Bio,Stats
import pandas as pd

with Session(engine) as session:
    statement = (
        select(Bio.first_name, Bio.last_name, Bio.position, Stats.PTS)
        .join(Stats, (Stats.first_name == Bio.first_name) & (Stats.last_name == Bio.last_name))
        .where(Stats.PTS > 10)
    )
    records = session.exec(statement).all()

records_df = pd.DataFrame(records)
print(records_df)