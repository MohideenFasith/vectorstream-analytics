from datetime import datetime, timedelta, timezone
from .models import Event, EventIn
from .store import EventStore
from .aggregation import aggregate

class AnalyticsService:
    def __init__(self): self.store=EventStore()
    def ingest(self,item:EventIn)->dict:
        event=Event(**item.model_dump()); created=self.store.put(event)
        return {"accepted":created,"id":event.id}
    def query(self,stream:str,window_seconds:int,dimension:str|None=None,start:datetime|None=None,end:datetime|None=None):
        return aggregate(self.store.list(stream,start,end),window_seconds,dimension)
    def retain(self,hours:int)->int:
        if hours<0: raise ValueError("hours must be >= 0")
        return self.store.delete_before(datetime.now(timezone.utc)-timedelta(hours=hours))
