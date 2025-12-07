import pytest, asyncio
from app.events.publisher import EventPublisher

@pytest.mark.asyncio
async def test_publish_succeeds():
    pub = EventPublisher()
    await pub.publish("test.subject", {"ping": "pong"})
    assert True  # if no exception, works
