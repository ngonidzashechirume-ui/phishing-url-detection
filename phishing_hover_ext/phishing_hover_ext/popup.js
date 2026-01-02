// popup.js
document.getElementById("predict-btn").addEventListener("click", async () => {
    const url = document.getElementById("test-url").value.trim();
    const statusDiv = document.getElementById("status");

    if (!url) {
        statusDiv.textContent = "⚠️ Please enter a URL.";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        const data = await response.json();
        if (data.prediction === 1) {
            statusDiv.textContent = "🚨 Phishing detected!";
            statusDiv.style.color = "red";
        } else {
            statusDiv.textContent = "✅ Safe link.";
            statusDiv.style.color = "green";
        }
    } catch (err) {
        statusDiv.textContent = "❌ Backend not running.";
        statusDiv.style.color = "gray";
    }
});
