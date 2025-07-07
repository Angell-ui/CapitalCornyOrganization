import asyncio
import aiohttp
import base64
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("deepgram-test")

DEEPGRAM_API_KEY = "YOUR_DEEPGRAM_API_KEY"  # replace this with your real key
DEEPGRAM_WS_URL = "wss://api.deepgram.com/v1/listen?punctuate=true"

# Example: load some raw audio bytes to send (replace with your own raw PCM or opus audio)
# For test purposes, we’ll just send dummy data here, real audio will produce better results
dummy_audio_payload = base64.b64encode(b"\x00" * 3200).decode("ascii")

async def deepgram_test():
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(DEEPGRAM_WS_URL, headers=headers) as ws:
            logger.info("Connected to Deepgram WebSocket")

            # Send dummy audio payload wrapped as JSON per Deepgram spec
            audio_message = json.dumps({
                "type": "Binary",
                "media": {
                    "payload": dummy_audio_payload
                }
            })

            await ws.send_bytes(base64.b64decode(dummy_audio_payload))
            logger.info("Sent dummy audio bytes")

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    logger.info(f"Received message: {msg.data}")
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {ws.exception()}")
                    break

asyncio.run(deepgram_test())
