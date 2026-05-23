(function () {
  const form = document.getElementById("scan-form");
  const resultEl = document.getElementById("scan-result");
  const submitBtn = form && form.querySelector('button[type="submit"]');

  if (!form || !resultEl) return;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const urlInput = form.querySelector('input[name="name"]');
    const url = urlInput && urlInput.value.trim();
    if (!url) return;

    const apiBase = (window.PHISH_API_URL || "").replace(/\/$/, "");
    if (!apiBase || apiBase.includes("YOUR-RENDER-APP")) {
      resultEl.innerHTML =
        '<p class="text-danger">Set <code>PHISH_API_URL</code> in Netlify to your Render backend URL.</p>';
      return;
    }

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = "Scanning…";
    }
    resultEl.innerHTML = "<p>Analyzing URL, this may take up to 30 seconds…</p>";

    try {
      const res = await fetch(apiBase + "/api/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url }),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || "Scan failed");
      }
      const btnClass = data.isSafe ? "button1" : "button2";
      resultEl.innerHTML =
        "<b><p>" +
        escapeHtml(data.url) +
        "</p></b>" +
        '<h2 style="color:blue;">Website is ' +
        escapeHtml(data.verdict) +
        " to use</h2><br>" +
        '<button class="' +
        btnClass +
        '" type="button" id="continue-btn">' +
        escapeHtml(data.buttonText) +
        "</button><br>";
      const continueBtn = document.getElementById("continue-btn");
      if (continueBtn) {
        continueBtn.addEventListener("click", function () {
          window.open(data.url, "_blank", "noopener,noreferrer");
        });
      }
    } catch (err) {
      resultEl.innerHTML =
        '<p class="text-danger">Error: ' + escapeHtml(err.message) + "</p>";
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = "Scan URL";
      }
    }
  });

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }
})();
