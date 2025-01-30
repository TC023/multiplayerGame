# server.py
from aiohttp import web, WSMsgType

app = web.Application()
players = {}  # Stores player positions

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    player_id = None

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                data = msg.json()
                if "update" in data:
                    # Update player position
                    player_id = data["update"]["id"]
                    players[player_id] = data["update"]["pos"]
                    # Broadcast to all clients
                    await ws.send_json({"players": players})
                    print(players)
                elif "delete" in data:
                    del players[data["delete"]]
    finally:
        if player_id and player_id in players:
            del players[player_id]
        await ws.close()
    return ws

async def get_players(request):
    return web.json_response({"players": players})

app.add_routes([
    web.get("/ws", websocket_handler),
    web.get("/players", get_players)
    ])

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=5000)