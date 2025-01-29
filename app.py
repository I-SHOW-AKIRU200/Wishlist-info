from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# API Endpoint to fetch wishlist data
@app.route('/fetch_wishlist', methods=['GET'])
def fetch_wishlist():
    uid = request.args.get("uid")
    region = request.args.get("region")

    if not uid and not region:
        return jsonify({"error": "Please provide either UID or Region"}), 400

    api_url = f"https://ariflex-labs-wishlist-api.vercel.app/items_info?uid={uid}&region={region}"

    try:
        response = requests.get(api_url)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve HTML directly from Python
@app.route('/akiru-wishlist-info-web')
def wishlist_page():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AKIRU Wishlist Info</title>
    <style>
        body { font-family: 'Arial', sans-serif; margin: 0; padding: 0; background-color: #f1f5f9; color: #333; }
        .container { max-width: 900px; margin: 50px auto; background: #fff; border-radius: 10px; padding: 30px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); }
        h1 { text-align: center; color: #4A90E2; font-size: 2.5rem; margin-bottom: 20px; }
        .input-group { display: flex; justify-content: space-between; gap: 10px; margin-bottom: 20px; }
        input, button { padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; width: 48%; }
        button { background-color: #4A90E2; color: white; cursor: pointer; width: 48%; border: none; }
        button:hover { background-color: #007bff; }
        .wishlist { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; margin-top: 30px; }
        .item { background: #000; padding: 20px; border-radius: 8px; border: 1px solid #ddd; color: white; }
        .item h3 { margin: 0 0 10px; color: #007bff; }
        .item-image { width: 100%; height: 200px; object-fit: contain; border-radius: 8px; margin-top: 15px; }
        .error { color: red; font-weight: bold; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AKIRU Wishlist Info</h1>
        <div class="input-group">
            <input type="text" id="uidInput" placeholder="Enter UID">
            <input type="text" id="regionInput" placeholder="Enter Region">
            <button id="fetchButton">Fetch Wishlist</button>
        </div>
        <div id="wishlist"></div>
        <div id="loading" class="loading" style="display: none;">Loading...</div>
    </div>

    <script>
        document.getElementById("fetchButton").addEventListener("click", () => {
            const uid = document.getElementById("uidInput").value.trim();
            const region = document.getElementById("regionInput").value.trim();
            const wishlistContainer = document.getElementById("wishlist");
            const loadingSpinner = document.getElementById("loading");

            if (!uid && !region) {
                wishlistContainer.innerHTML = "<p class='error'>Please enter either UID or Region.</p>";
                return;
            }

            wishlistContainer.innerHTML = "";
            loadingSpinner.style.display = "block";

            fetch("/fetch_wishlist?uid=" + uid + "&region=" + region)
                .then(response => response.json())
                .then(data => {
                    wishlistContainer.innerHTML = "";
                    if (data.items && data.items.length > 0) {
                        data.items.forEach(item => {
                            const itemElement = document.createElement("div");
                            itemElement.className = "item";
                            const imageUrl = `https://ff-community-api.vercel.app/icons?id=${item.itemId}`;

                            itemElement.innerHTML = `
                                <h3>Item ID: ${item.itemId}</h3>
                                <img src="${imageUrl}" alt="Item Image" class="item-image">
                            `;

                            wishlistContainer.appendChild(itemElement);
                        });
                    } else {
                        wishlistContainer.innerHTML = "<p>No items found.</p>";
                    }
                    loadingSpinner.style.display = "none";
                })
                .catch(error => {
                    wishlistContainer.innerHTML = `<p class='error'>Error: ${error.message}</p>`;
                    loadingSpinner.style.display = "none";
                });
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
