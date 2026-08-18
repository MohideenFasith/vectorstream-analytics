from datetime import datetime
from .models import Event

class EventStore:
    def __init__(self): self._events:dict[str,Event]={}
    def put(self,event:Event)->bool:
        if event.id in self._events:return False
        self._events[event.id]=event; return True
    def list(self,stream:str,start:datetime|None=None,end:datetime|None=None)->list[Event]:
        out=[e for e in self._events.values() if e.stream==stream and (start is None or e.ts>=start) and (end is None or e.ts<end)]
        return sorted(out,key=lambda e:e.ts)
    def delete_before(self,cutoff:datetime)->int:
        ids=[k for k,e in self._events.items() if e.ts<cutoff]
        for k in ids:del self._events[k]
        return len(ids)
