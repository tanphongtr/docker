import asyncio
import json
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from redis import asyncio as redis

app = FastAPI()

REDIS_URL = "redis://redis:6379"
CHANNEL_NAME = "sse_channel"
connections = {}
INSTANCE_ID = str(uuid.uuid4())  # 🔑 định danh duy nhất cho mỗi instance


@app.get("/sse/{client_id}")
async def sse_endpoint(client_id: str):
    if client_id in connections:
        del connections[client_id]
    queue = asyncio.Queue()
    connections[client_id] = queue

    async def event_stream():
        try:
            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n"
        except asyncio.CancelledError:
            if client_id in connections:
                del connections[client_id]

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/webhook")
async def receive_webhook(request: Request):
    payload = await request.json()
    client_id = payload.get("client_id")

    # Gắn source_id để tránh duplicate khi nhận từ Redis
    message = {
        "source_id": INSTANCE_ID,
        "data": payload,
    }

    # Gửi trực tiếp nếu client đang kết nối hiện tại
    if client_id:
        # nếu có client_id cụ thể, gửi tới client đó nếu đang kết nối
        if client_id in connections:
            await connections[client_id].put(payload)
    else:
        # nếu không truyền client_id trong hook, broadcast tới tất cả client đang kết nối
        if connections:
            # snapshot các queue để tránh thay đổi dict trong lúc lặp
            queues = list(connections.values())
            await asyncio.gather(*(q.put(payload) for q in queues))

    # Publish để các instance khác cùng nhận
    r = await redis.from_url(REDIS_URL, decode_responses=True)
    await r.publish(CHANNEL_NAME, json.dumps(message))
    await r.close()

    return {"status": "ok"}


async def redis_subscriber():
    r = await redis.from_url(REDIS_URL, decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe(CHANNEL_NAME)

    async for message in pubsub.listen():
        if message["type"] == "message":
            msg = json.loads(message["data"])
            # Bỏ qua nếu message đến từ chính instance này
            if msg.get("source_id") == INSTANCE_ID:
                continue

            payload = msg["data"]
            client_id = payload.get("client_id")
            if client_id:
                if client_id in connections:
                    await connections[client_id].put(payload)
            else:
                # broadcast tới tất cả client đang kết nối nếu message không có client_id
                if connections:
                    queues = list(connections.values())
                    await asyncio.gather(*(q.put(payload) for q in queues))


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(redis_subscriber())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
