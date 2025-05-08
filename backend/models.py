from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Float, DateTime

class TCMBReserve(BaseModel):
    id =  Column(Integer, primary_key=True, index=True)
    source = Column(String)
    symbol = Column(String)
    value = Column(Float)
    delta = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)