from sqlmodel import Session, select
from models import engine,Bio
import pandas as pd
from sqlalchemy import func

with Session(engine) as session:
    statement = (
        select(Bio.position,func.avg(Bio.weight).label("average_weight"))
        .group_by(Bio.position)
        .order_by(func.avg(Bio.weight).desc())
    )
    results = session.exec(statement).all()
    
    
for result in results:
    print(result)
    


