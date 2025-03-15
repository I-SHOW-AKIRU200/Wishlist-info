from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)

WISHLIST_API = "https://ariflex-labs-wishlist-api.vercel.app/items_info?uid={uid}&region={region}"
ICON_API = "https://system.ffgarena.cloud/api/iconsff?image={item_id}.png"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fetch_wishlist", methods=["POST"])
def fetch_wishlist():
    uid = request.form.get("uid")
    region = request.form.get("region")

    if not uid or not region:
        return jsonify({"error": "UID and Region are required!"})

    api_url = WISHLIST_API.format(uid=uid, region=region)

    try:
        response = requests.get(api_url, timeout=25)  # Wait for API response
        data = response.json()

        if "items" not in data:
            return jsonify({"error": "Invalid API response!"})

        items = [
            {
                "image_url": ICON_API.format(item_id=item["itemId"]),
                "release_time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(item["releaseTime"])),
            }
            for item in data["items"]
        ]

        return jsonify({"items": items})

    except Exception as e:
        return jsonify({"error": f"API error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
