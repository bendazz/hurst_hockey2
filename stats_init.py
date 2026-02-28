from sqlmodel import Session
from models import engine
from stats_instances import generate_stats_instances

with Session(engine) as session:
    stats = generate_stats_instances()
    session.add_all(stats)
    session.commit()

