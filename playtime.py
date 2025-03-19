from datetime import datetime as dt
import json

with open("chat.json", "r") as f:
    chat = json.load(f)
    
messages = chat["messages"]

playerData = {}

# for msg in messages:
#     if msg["author"]["name"] == "Minecraft Chat Sync":
#         try:
#             info_msg = msg["embeds"][0]["author"]["name"]
#             if "joined the server" in info_msg:
#                 name = info_msg.split(" ")[0]
#                 if name not in playerData:
#                     playerData[name] = {"joins": 1, "leaves": 0}
#                 else:
#                     playerData[name]["joins"] += 1
#             elif "left the server" in info_msg:
#                 name = info_msg.split(" ")[0]
#                 if name not in playerData:
#                     playerData[name] = {"joins": 0, "leaves": 1}
#                 else:
#                     playerData[name]["leaves"] += 1
#         except:
#             pass

# for player in playerData:
#     print(f"{player}\n    Joins: {playerData[player]['joins']}\n    Leaves: {playerData[player]['leaves']}")

for msg in messages:
    try:
        if msg["author"]["name"] == "Minecraft Chat Sync":
            info_msg = msg["embeds"][0]["author"]["name"]
            playerName = info_msg.split(" ")[0]
            joined = "joined the server" in info_msg
            left = "left the server" in info_msg
            if joined or left:
                if playerName not in playerData:
                    playerData[playerName] = {"data": []}
                interactionType = "j" if joined else "l"
                unixTimestamp = dt.fromisoformat(msg["timestamp"]).timestamp()
                playerData[playerName]["data"].append((interactionType, unixTimestamp))
    except:
        pass

for player in playerData:
    # Remove duplicates (joins without leaves)
    data = playerData[player]["data"]
    i = 0
    while i < len(data) - 1:
        if data[i][0] == data[i + 1][0]:
            data.pop(i)
        else:
            i += 1
    # Count up playtime
    playtime = 0
    playerData[player]["sessions"] = []
    for i in range(0, len(playerData[player]["data"]), 2):
        try:
            joinTime = playerData[player]["data"][i][1]
            leaveTime = playerData[player]["data"][i+1][1]
            sessionLength = leaveTime - joinTime
            playtime += sessionLength
            playerData[player]["sessions"].append(sessionLength)
        except:
            pass
    playerData[player]["playtime"] = playtime

for player in playerData:
    avg = 0
    for session in playerData[player]["sessions"]:
        avg += session
    avg /= len(playerData[player]["sessions"])
    print(f"{player} played for {round(playerData[player]['playtime']/60/60, 2)} hours\n    Average session: {round(avg/60, 1)} minutes.")
