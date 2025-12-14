const $ = (id) => document.getElementById(id);

function msg(text, type="") {
  const el = $("msg");
  el.className = "msg " + (type || "");
  el.textContent = text || "";
}

function getUserId() {
  return ($("userId").value || "1").trim();
}

async function apiGet(path) {
  const res = await fetch(path, { headers: { "X-User-Id": getUserId() } });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function apiPost(path, body) {
  const res = await fetch(path, {
    method: "POST",
    headers: {
      "X-User-Id": getUserId(),
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body)
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// If you have DELETE route, we’ll call it. If not, you can add later.
async function apiDelete(path) {
  const res = await fetch(path, {
    method: "DELETE",
    headers: { "X-User-Id": getUserId() }
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function fmtUSD(x) {
  if (x === null || x === undefined) return "—";
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(x);
}

function changeClass(val) {
  if (val === null || val === undefined) return "neutral";
  if (val > 0) return "good";
  if (val < 0) return "bad";
  return "neutral";
}

async function loadCoins() {
  msg("Loading favourites…");
  const list = $("list");
  list.innerHTML = "";

  const data = await apiGet("/coins");
  const items = data.items || [];
  $("count").textContent = items.length;

  $("empty").style.display = items.length ? "none" : "block";


  for (const c of items) {
    const card = document.createElement("div");
    card.className = "coin";
    card.innerHTML = `
      <div class="coinTop">
        <div>
          <div class="coinName">${c.name || c.symbol?.toUpperCase() || "Coin"}</div>
          <div class="coinSym">${(c.symbol || "").toLowerCase()}</div>
        </div>
        <button class="btn danger">Remove</button>
      </div>
      <div class="price">—</div>
      <div class="change neutral">—</div>
    `;

    // Remove button (only works if you have DELETE endpoint)
    card.querySelector("button").onclick = async () => {
      try {
        // If your DELETE route is like /coins/<symbol>:
        await apiDelete(`/coins/${encodeURIComponent(c.symbol)}`);
        msg("Removed.", "ok");
        await loadCoins();
      } catch (e) {
        msg("Remove failed (maybe DELETE route not implemented yet).", "err");
      }
    };

    list.appendChild(card);

   
    const map = { btc: "bitcoin", eth: "ethereum", sol: "solana", ada: "cardano", xrp: "ripple", doge: "dogecoin" };
    const coinId = map[(c.symbol || "").toLowerCase()];
    if (!coinId) continue;

    try {
      const info = await fetch(`/coins/${coinId}/external-info`).then(r => r.json());
      const d = info.data || {};
      const price = d.current_price_usd;
      const chg = d.price_change_24h;

      card.querySelector(".price").textContent = fmtUSD(price);
      const ch = card.querySelector(".change");
      ch.className = "change " + changeClass(chg);
      ch.textContent = (chg === null || chg === undefined) ? "—" : `${chg.toFixed(2)}% (24h)`;
    } catch {}
  }

  msg("Done.", "ok");
}

async function addCoin() {
  const symbol = ($("symbolInput").value || "").trim().toLowerCase();
  if (!symbol) return msg("Type a symbol first (btc, eth, sol).", "err");

  msg("Adding…");
  try {
    await apiPost("/coins", { symbol });
    $("symbolInput").value = "";
    msg("Added!", "ok");
    await loadCoins();
  } catch (e) {
    msg("Add failed. Check symbol / backend response.", "err");
  }
}

$("loadBtn").onclick = () => loadCoins().catch(e => msg("Load failed.", "err"));
$("addBtn").onclick = () => addCoin().catch(e => msg("Add failed.", "err"));

// Auto-load on open

loadCoins().catch(() => {});
