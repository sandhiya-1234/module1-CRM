import asyncio
from nats.aio.client import Client as NATS

async def test():
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4222"])
    await nc.publish("test.subject", b"hello from lavaa")
    await nc.flush()
    print("✅ NATS connection & publish OK")
    await nc.close()

asyncio.run(test())
