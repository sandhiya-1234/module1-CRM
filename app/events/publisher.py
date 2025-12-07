import asyncio
import json
from nats.aio.client import Client as NATS

class EventPublisher:
    def __init__(self, servers="nats://localhost:4222"):
        self.servers = servers

    async def _publish_async(self, subject: str, payload: dict):
        """Internal async method that actually publishes the message."""
        try:
            nc = NATS()
            await nc.connect(servers=[self.servers])

            print(f"🚀 Sending event on '{subject}': {payload}")
            await nc.publish(subject, json.dumps(payload).encode())
            await nc.flush()
            print(f"✅ NATS event published successfully on '{subject}'")

            await nc.close()
        except Exception as e:
            print(f"❌ Failed to publish event: {e}")

    def publish(self, subject: str, payload: dict):
        """Universal publisher: works from both sync & async contexts."""
        try:
            loop = asyncio.get_running_loop()
            # If already inside async environment → schedule it
            loop.create_task(self._publish_async(subject, payload))
        except RuntimeError:
            # No loop running → run a fresh event loop
            asyncio.run(self._publish_async(subject, payload))
