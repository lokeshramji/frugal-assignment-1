from pathlib import Path
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title='Q1 Canvas/WebSocket Testbed')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

@app.get('/')
async def index():
    return FileResponse(BASE_DIR / 'index.html')

@app.websocket('/ws')
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        await ws.send_text(json.dumps({'type':'state','state':'loading','target':None,'balance':100}))
        while True:
            data = json.loads(await ws.receive_text())
            if data.get('type') == 'ready':
                await asyncio.sleep(0.15)
                await ws.send_text(json.dumps({'type':'state','state':'active','target':{'x':410,'y':230},'balance':100}))
            elif data.get('type') == 'corrupt':
                await ws.send_text(json.dumps({'type':'state','state':'active','target':{'x':410,'y':230},'balance':1e7}))
            elif data.get('type') == 'ping':
                await ws.send_text(json.dumps({'type':'pong'}))
    except (WebSocketDisconnect, Exception):
        return

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
