from datetime import datetime
from fastapi import FastAPI,Query
from .models import EventIn
from .service import AnalyticsService
app=FastAPI(title="VectorStream Analytics",version="0.1.0"); service=AnalyticsService()
@app.get("/health")
def health():return {"status":"ok"}
@app.post("/events",status_code=202)
def ingest(e:EventIn):return service.ingest(e)
@app.get("/aggregate/{stream}")
def query(stream:str,window_seconds:int=Query(60,gt=0),dimension:str|None=None,start:datetime|None=None,end:datetime|None=None):return service.query(stream,window_seconds,dimension,start,end)
@app.delete("/retention")
def retention(hours:int=Query(24,ge=0)):return {"deleted":service.retain(hours)}
