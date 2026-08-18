from datetime import datetime,timezone
from vectorstream.models import EventIn
from vectorstream.service import AnalyticsService

def test_dedupe_and_aggregate():
    s=AnalyticsService(); ts=datetime(2026,1,1,tzinfo=timezone.utc)
    e=EventIn(id="a",stream="orders",ts=ts,value=10,dimensions={"region":"in"})
    assert s.ingest(e)["accepted"] is True
    assert s.ingest(e)["accepted"] is False
    s.ingest(EventIn(id="b",stream="orders",ts=ts,value=20,dimensions={"region":"in"}))
    rows=s.query("orders",60,"region")
    assert rows[0]["sum"]==30 and rows[0]["count"]==2
