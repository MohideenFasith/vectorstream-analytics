from collections import defaultdict
from datetime import datetime, timezone
from .models import Event

def epoch_seconds(ts:datetime)->int:
    if ts.tzinfo is None: ts=ts.replace(tzinfo=timezone.utc)
    return int(ts.timestamp())

def aggregate(events:list[Event],window_seconds:int,dimension:str|None=None)->list[dict]:
    if window_seconds<=0: raise ValueError("window_seconds must be positive")
    buckets=defaultdict(list)
    for e in events:
        start=(epoch_seconds(e.ts)//window_seconds)*window_seconds
        group=e.dimensions.get(dimension,"__missing__") if dimension else "all"
        buckets[(start,group)].append(e.value)
    rows=[]
    for (start,group),vals in sorted(buckets.items()):
        rows.append({"window_start":datetime.fromtimestamp(start,tz=timezone.utc).isoformat(),"group":group,"count":len(vals),"sum":round(sum(vals),6),"avg":round(sum(vals)/len(vals),6),"min":min(vals),"max":max(vals)})
    return rows
