import json

with open("chat.json", "r") as f:
    chat = json.load(f)
    
messages = chat["messages"]

playerData = {}

for msg in messages:
    try:
        if msg["author"]["name"] == "Minecraft Chat Sync":
            info_msg = msg["embeds"][0]["author"]["name"]
            try:
                info_color = msg["embeds"][0]["color"]
            except:
                info_color = None
            if info_color == None:
                name = info_msg.split(" ")[0]
                if name not in playerData:
                    playerData[name] = {"deaths": 0}  # Initialize "deaths" to 0
                playerData[name]["deaths"] += 1  
    except:
        pass

for player in playerData:
    print(f"{player} died {playerData[player]['deaths']} times")
