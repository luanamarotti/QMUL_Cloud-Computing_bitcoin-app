# Bitcoin App – External REST API Integration

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
