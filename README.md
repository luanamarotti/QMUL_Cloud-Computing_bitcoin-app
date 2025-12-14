# Crypto Favourites App (Flask + REST + CoinGecko)

A Flask-based cryptocurrency favourites application that allows users to manage a personal watchlist of crypto coins and view live market data using the public CoinGecko API.

The project demonstrates:
- RESTful CRUD API design
- External API integration
- Persistent database storage
- Simple frontend UI
- Cloud computing concepts

---

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
