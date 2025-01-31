from flask import Flask, request, jsonify, render_template_string
import requests
import time

app = Flask(__name__)

API_KEY = "ADITYA"
API_URL = "https://player-info-final.vercel.app"
OUTFIT_API_URL = "https://ff-community-api.vercel.app/icons?id={}"

def format_timestamp(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp))) if timestamp else "N/A"

@app.route("/akiru-free-fire-info-web")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Akiru Free Fire Info</title>
        <style>
            body {
                font-family: monospace;
                text-align: center;
                background-color: #222;
                color: #fff;
                padding: 20px;
            }
            .container {
                max-width: 700px;
                margin: auto;
                background: #333;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(255,255,255,0.2);
            }
            textarea {
                width: 100%;
                height: 400px;
                background: #111;
                color: #0f0;
                border: none;
                padding: 10px;
                font-size: 14px;
                resize: none;
            }
            button {
                background-color: #007bff;
                color: white;
                padding: 10px;
                border: none;
                margin-top: 10px;
                cursor: pointer;
            }
            input {
                padding: 5px;
                margin: 5px;
                width: 90%;
            }
            .outfit-grid, .wishlist-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
                margin-top: 20px;
            }
            .outfit-grid img, .wishlist-grid img {
                width: 100px;
                height: 100px;
                background: #444;
                border-radius: 5px;
                padding: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Akiru Free Fire Info</h2>
            <input type="text" id="uid" placeholder="Enter UID">
            <input type="text" id="region" placeholder="Enter Region">
            <button onclick="fetchPlayerInfo()">Get Info</button>
            <textarea id="player-data" readonly></textarea>
            <div id="outfit-grid" class="outfit-grid"></div>

            <button onclick="fetchWishlistInfo()">Get Wishlist Info</button>
            <textarea id="wishlist-data" readonly></textarea>
            <div id="wishlist-grid" class="wishlist-grid"></div>
        </div>

        <script>
            function fetchPlayerInfo() {
                const uid = document.getElementById("uid").value;
                const region = document.getElementById("region").value;

                fetch('/akiru-free-fire-info-web/player-info', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: `uid=${uid}&region=${region}`
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("player-data").value = data.text;
                    showOutfits(data.outfits);
                })
                .catch(error => console.error('Error:', error));
            }

            function showOutfits(outfits) {
                const grid = document.getElementById("outfit-grid");
                grid.innerHTML = "";
                outfits.forEach(url => {
                    const img = document.createElement("img");
                    img.src = url;
                    grid.appendChild(img);
                });
            }

            function fetchWishlistInfo() {
                const uid = document.getElementById("uid").value;
                const region = document.getElementById("region").value;

                fetch('/akiru-free-fire-info-web/wishlist-info', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: `uid=${uid}&region=${region}`
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("wishlist-data").value = data.text;
                    showWishlistItems(data.items);
                })
                .catch(error => console.error('Error:', error));
            }

            function showWishlistItems(items) {
                const grid = document.getElementById("wishlist-grid");
                grid.innerHTML = ""; // Clear the grid before adding new images

                items.forEach(item => {
                    const img = document.createElement("img");
                    img.src = `https://ff-community-api.vercel.app/icons?id=${item.itemId}`;
                    grid.appendChild(img);
                });
            }
        </script>
    </body>
    </html>
    """)

@app.route("/akiru-free-fire-info-web/player-info", methods=["POST"])
def player_info():
    uid = request.form.get("uid")
    region = request.form.get("region")

    if not uid or not region:
        return jsonify({"text": "Error: UID and Region are required."}), 400

    response = requests.get(f"{API_URL}?region={region}&uid={uid}&key={API_KEY}")

    if response.status_code != 200:
        return jsonify({"text": "Error: Failed to fetch data."}), response.status_code

    data = response.json()
    
    account_info = data.get("basicInfo", {})
    captain_info = data.get("captainBasicInfo", {})
    clan_info = data.get("clanBasicInfo", {})
    pet_info = data.get("petInfo", {})
    social_info = data.get("socialInfo", {})
    outfit_ids = data.get("profileInfo", {}).get("clothes", [])

    formatted_response = f"""
╔════════════════════════════════════╗
║                 𝗙𝗥𝗘𝗘 𝗙𝗜𝗥𝗘 𝗣𝗟𝗔𝗬𝗘𝗥 𝗜𝗡𝗙𝗢
╚════════════════════════════════════╝
┌ 👨‍💻 ACCOUNT BASIC INFO 
    ├─ Name: {account_info.get('nickname', 'N/A')}
    ├─ UID: {captain_info.get('accountId', 'N/A')}
    ├─ Level: {account_info.get('level', 'N/A')} (Exp: {account_info.get('exp', 'N/A')})
    ├─ Region: {account_info.get('region', 'N/A')}
    ├─ Likes: {account_info.get('liked', 'N/A')}
    ├─ Celebrity Status: {"True" if account_info.get('accountType') == "1" else "False"}
    ├─ Title: {account_info.get('title', 'N/A')}
    └─ Signature: {social_info.get('signature', 'N/A')}

┌ 🎮 ACCOUNT ACTIVITY 
    ├─ Most Recent OB: {account_info.get('releaseVersion', 'N/A')}
    ├─ Fire Pass: {"Elite" if account_info.get('hasElitePass') else "Basic"}
    ├─ BR Rank: {account_info.get('maxRank', 'N/A')} (Points: {account_info.get('rankingPoints', 'N/A')})
    ├─ CS Points: {account_info.get('csRankingPoints', 'N/A')}
    └─ Last Login: {format_timestamp(account_info.get('lastLoginAt', 0))}

┌ 👕 ACCOUNT OVERVIEW 
    ├─ Avatar ID: {account_info.get('headPic', 'N/A')}
    ├─ Equipped Banner: {account_info.get('bannerId', 'N/A')}
    ├─ Equipped Weapons: {', '.join(account_info.get('weaponSkinShows', []))}
    └─ Equipped Skills: {', '.join([str(skill['skillId']) for skill in data.get('profileInfo', {}).get('equipedSkills', [])])}

┌ 🐾 PET DETAILS 
    ├─ Pet Name: {pet_info.get('name', 'N/A')}
    ├─ Pet Exp: {pet_info.get('exp', 'N/A')}
    └─ Pet Level: {pet_info.get('level', 'N/A')}

┌ 🛡️ GUILD INFO 
    ├─ Guild Name: {clan_info.get('clanName', 'N/A')}
    ├─ Guild Level: {clan_info.get('clanLevel', 'N/A')}
═════════════════════════════════════
Don't Forget To Join Our Telegram Group For More Info
   └─ https://t.me/IShowAkiru5
"""

    outfit_urls = [OUTFIT_API_URL.format(outfit_id) for outfit_id in outfit_ids]

    return jsonify({"text": formatted_response, "outfits": outfit_urls})

@app.route("/akiru-free-fire-info-web/wishlist-info", methods=["POST"])
def wishlist_info():
    uid = request.form.get("uid")
    region = request.form.get("region")

    if not uid or not region:
        return jsonify({"text": "Error: UID and Region are required."}), 400

    # Fetch wishlist data from the given API
    wishlist_url = f"https://player-info-final.vercel.app/ADITYA-PLAYER-INFO?uid={uid}&region={region}"
    response = requests.get(wishlist_url)

    if response.status_code != 200:
        return jsonify({"text": "Error: Failed to fetch wishlist data."}), response.status_code

    data = response.json()

    # Extract item details
    items = data.get("items", [])
    item_urls = []
    
    # Generate URLs for item images using the itemId
    for item in items:
        item_id = item.get("itemId")
        item_urls.append({
            "itemId": item_id,
            "releaseTime": item.get("releaseTime"),
            "imageUrl": f"https://ff-community-api.vercel.app/icons?id={item_id}"
        })
    
    # Format the response to show wishlist items and images
    wishlist_text = "Wishlist Items:\n" + "\n".join([f"- Item ID: {item['itemId']} (Release: {format_timestamp(item['releaseTime'])})" for item in items])

    return jsonify({
        "text": wishlist_text,
        "items": item_urls
    })

if __name__ == "__main__":
    app.run(debug=True)
