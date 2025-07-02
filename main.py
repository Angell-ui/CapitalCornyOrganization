from quart import Quart, websocket
import logging

app = Quart(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/")
async def index():
    return "Hello! WebSocket test server is running."

@app.websocket("/ws/audio")
async def ws_audio():
    logger.info("WebSocket connection received")
    call_sid = websocket.args.get("call_sid")
    logger.info(f"Call SID from query: {call_sid}")

    try:
        async for message in websocket:
            logger.info(f"Received message: {message}")
            await websocket.send(f"Echo: {message}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

if __name__ == "__main__":
    app.run(port=10000)
