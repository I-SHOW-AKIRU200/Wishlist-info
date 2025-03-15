document.getElementById("search-btn").addEventListener("click", function() {
    const uid = document.getElementById("uid").value;
    const region = document.getElementById("region").value;
    const loading = document.querySelector(".loading");
    const container = document.getElementById("wishlist-container");

    if (!uid || !region) {
        alert("Please enter UID and Region");
        return;
    }

    loading.style.display = "block";
    container.innerHTML = "";

    fetch("/fetch_wishlist", {
        method: "POST",
        body: new URLSearchParams({ uid, region }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
    .then(response => response.json())
    .then(data => {
        loading.style.display = "none";

        if (data.error) {
            container.innerHTML = `<p>${data.error}</p>`;
            return;
        }

        data.items.forEach(item => {
            const div = document.createElement("div");
            div.classList.add("item");

            div.innerHTML = `
                <img src="${item.image_url}" width="100">
                <p>Release Time: ${item.release_time}</p>
                <img src="static/images/watermark.png" class="watermark">
            `;
            container.appendChild(div);
        });
    })
    .catch(error => {
        loading.style.display = "none";
        container.innerHTML = `<p>Error fetching data!</p>`;
    });
});
