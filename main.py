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
    app.logger.info("WebSocket connection received")
    call_sid = websocket.args.get("call_sid")
    app.logger.info(f"Call SID from query: {call_sid}")

    try:
        while True:
            message = await websocket.receive()
            app.logger.info(f"Received message: {message}")
            await websocket.send(f"Echo: {message}")
    except Exception as e:
        app.logger.error(f"WebSocket error: {e}")