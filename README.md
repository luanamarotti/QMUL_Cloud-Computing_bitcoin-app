# Crypto Favourites App (Flask + REST + CoinGecko)

A Flask-based cryptocurrency favourites application that allows users to manage a personal watchlist of crypto coins and view live market data using the public CoinGecko API.

The project demonstrates:
- RESTful CRUD API design
- External API integration
- Persistent database storage
- Simple frontend UI
- Cloud computing concepts

---
### Bitcoin App – External REST API Integration

This project is a Flask-based Bitcoin/Crypto application that integrates with the public **CoinGecko API** to retrieve:

- Live cryptocurrency prices (`GET /coins/live-prices`)
- Detailed coin metadata (`GET /coins/<id>/external-info`)

The project includes:

### ✔ External API Integration
- Helper function `fetch_external_coin_data()` that connects to CoinGecko  
- Error handling for timeouts, network issues, invalid JSON, and API errors  
- Clean JSON responses returned through Flask endpoints  

### ✔ Hash-Based Authentication (Security)
All external API endpoints are **protected** using a simple hash-based API key mechanism.  
To access any `/coins/*` endpoint, you must send the API key header:
X-API-KEY: my-very-secret-key-123


## Features

### Core Features
- REST-based CRUD API for user favourites:
  - `GET /coins` – List favourite coins
  - `POST /coins` – Add a favourite coin
  - `PUT /coins/<id>` – Update a favourite coin
  - `DELETE /coins/<id>` or `DELETE /coins/<symbol>` – Remove a favourite
- Multi-user support using request headers (`X-User-Id`)
- Persistent storage (SQLite locally / PostgreSQL in cloud setup)

### External API Integration
- CoinGecko public API (no authentication required)
- Live price data
- Detailed coin information

### Frontend UI
- Simple browser-based UI
- Add, view, and remove favourite coins
- Displays live prices fetched from CoinGecko

---

## Tech Stack
- **Backend:** Python, Flask
- **External API:** CoinGecko
- **Database:** SQLite (local) / PostgreSQL (cloud)
- **Frontend:** HTML, CSS, JavaScript (Flask templates)

---

## Project Structure
bitcoin-app/
app.py
api.py
db.py
external_api.py
templates/
index.html
static/
(optional CSS / JS)


---

## How to Run (Windows / PowerShell)

### 1) Create and activate virtual environment
```powershell
python -m venv venv
.\venv\Scripts\activate

2) Install dependencies
pip install -r requirements.txt

3) Run the application
python app.py


Open in browser:

http://127.0.0.1:5000

REST API Usage (CRUD)

All requests are user-specific using the header:

X-User-Id: 1

GET – List favourites
Invoke-RestMethod -Uri "http://127.0.0.1:5000/coins" -Method Get -Headers @{ "X-User-Id" = "1" }

POST – Add favourite (example: Bitcoin)
Invoke-RestMethod -Uri "http://127.0.0.1:5000/coins" -Method Post -Headers @{ "X-User-Id" = "1" } -ContentType "application/json" -Body '{"symbol":"btc"}'

PUT – Update favourite (example: favourite id 5 → Ethereum)
Invoke-RestMethod -Uri "http://127.0.0.1:5000/coins/5" -Method Put -Headers @{ "X-User-Id" = "1" } -ContentType "application/json" -Body '{"symbol":"eth"}'

DELETE – Remove favourite

Delete by favourite ID:

Invoke-RestMethod -Uri "http://127.0.0.1:5000/coins/5" -Method Delete -Headers @{ "X-User-Id" = "1" }


Delete by symbol (if enabled):

Invoke-RestMethod -Uri "http://127.0.0.1:5000/coins/btc" -Method Delete -Headers @{ "X-User-Id" = "1" }

External API Endpoints (CoinGecko)
Live prices
Invoke-RestMethod -Uri "http://127.0.0.1:5000/coins/live-prices" -Method Get

Coin details

Example:

Invoke-RestMethod -Uri "http://127.0.0.1:5000/coins/bitcoin/external-info" -Method Get

