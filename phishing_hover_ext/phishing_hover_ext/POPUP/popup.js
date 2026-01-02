document.getElementById("checkBtn").addEventListener("click", async () => {
    const url = document.getElementById("urlInput").value;
    const resultBox = document.getElementById("resultBox");

    if (!url) {
        resultBox.textContent = "⚠️ Please enter a URL.";
        resultBox.className = "phishing";
        resultBox.classList.remove("hidden");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url })
        });

        const data = await response.json();
        if (data.prediction === 1) {
            resultBox.textContent = "⚠️ Phishing detected!";
            resultBox.className = "phishing";
        } else {
            resultBox.textContent = "✅ Safe link.";
            resultBox.className = "safe";
        }
    } catch (err) {
        resultBox.textContent = "❌ Error contacting backend.";
        resultBox.className = "phishing";
    }

    resultBox.classList.remove("hidden");
});
