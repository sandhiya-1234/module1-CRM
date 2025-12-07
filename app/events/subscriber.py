import asyncio, json
from nats.aio.client import Client as NATS
from app.services.workflow_handlers import WorkflowHandlers

async def run_subscriber():
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4222"])

    async def message_handler(msg):
        try:
            data = json.loads(msg.data.decode())
            print(f"📬 Received on {msg.subject}: {data}")  # ✅ Debug log

            if msg.subject == "invoice.paid":
                await WorkflowHandlers.on_invoice_paid(data)
                print(f"✅ Workflow executed successfully for invoice {data.get('invoice_id')}")
        except Exception as e:
            print(f"❌ Error handling message: {e}")

    await nc.subscribe("invoice.paid", cb=message_handler)
    print("📡 Listening for invoice.paid events...")

    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("👋 Subscriber shutting down...")
    finally:
        await nc.close()

if __name__ == "__main__":
    asyncio.run(run_subscriber())
