from datetime import datetime, timezone
from pydantic import BaseModel, Field

class EventIn(BaseModel):
    id:str=Field(min_length=1,max_length=128)
    stream:str=Field(min_length=1,max_length=128)
    ts:datetime
    value:float
    dimensions:dict[str,str]=Field(default_factory=dict)

class Event(EventIn):
    received_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))
