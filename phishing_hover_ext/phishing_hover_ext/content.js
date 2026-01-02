// Caching to avoid repeated backend calls for the same URL
const urlPredictionCache = {};

// ML-based URL checker (calls Flask backend)
async function checkPhishingWithML(url) {
    if (urlPredictionCache[url] !== undefined) {
        return urlPredictionCache[url];
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        const result = await response.json();
        const isPhishing = result.prediction === 1;

        urlPredictionCache[url] = isPhishing;
        console.log("✅ ML result for", url, ":", isPhishing);
        return isPhishing;
    } catch (error) {
        console.error("❌ Error contacting ML backend:", error);
        return false;
    }
}

// Create and style popup
function createPopup(message, isPhishing, x, y) {
    // Remove existing
    const oldPopup = document.getElementById("hover-popup");
    if (oldPopup) oldPopup.remove();

    const popup = document.createElement("div");
    popup.textContent = message;
    popup.style.position = "absolute";
    popup.style.left = `${x + 10}px`;
    popup.style.top = `${y + 10}px`;
    popup.style.padding = "8px 12px";
    popup.style.borderRadius = "8px";
    popup.style.fontSize = "14px";
    popup.style.boxShadow = "0 0 8px rgba(0, 0, 0, 0.3)";
    popup.style.zIndex = "9999";
    popup.style.backgroundColor = isPhishing ? "#d9534f" : "#f0ad4e";
    popup.style.color = "white";
    popup.id = "hover-popup";

    document.body.appendChild(popup);
}

// Handle link hover
document.addEventListener("mouseover", function (event) {
    if (event.target.tagName === "A") {
        const url = event.target.href;
        const x = event.pageX;
        const y = event.pageY;

        checkPhishingWithML(url).then(isPhishing => {
            const msg = isPhishing
                ? "⚠️ Phishing detected!"
                : "✅ Looks safe.";
            createPopup(msg, isPhishing, x, y);
        });

        // Clean up on mouseout
        event.target.addEventListener("mouseout", () => {
            const popup = document.getElementById("hover-popup");
            if (popup) popup.remove();
        }, { once: true });
    }
});

// Handle click warning
document.addEventListener("click", function (event) {
    const target = event.target.closest("a");
    if (target && target.href) {
        const url = target.href;

        checkPhishingWithML(url).then(isPhishing => {
            if (isPhishing) {
                alert(`⚠️ WARNING: This link may be phishing!\n\n${url}`);
            }
        });
    }
});
