from flask import Blueprint, request, jsonify
from db import query_all, query_one, execute

coins_bp = Blueprint("coins", __name__)


def get_user_id():
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        return None
    try:
        return int(user_id)
    except ValueError:
        return None

@coins_bp.route("/coins", methods=["GET"])
def get_favourites():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "Missing or invalid X-User-Id header"}), 400

    sql = """
    SELECT
        f.id,
        c.symbol,
        c.name,
        f.added_at
    FROM favourites f
    JOIN coins c ON f.coin_id = c.id
    WHERE f.user_id = %s
    ORDER BY f.added_at DESC;
    """

    rows = query_all(sql, [user_id])
    return jsonify({"items": rows}), 200

@coins_bp.route("/coins", methods=["POST"])
def add_favourite():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "Missing or invalid X-User-Id header"}), 400

    data = request.get_json(silent=True)
    if not data or "symbol" not in data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    symbol = data["symbol"].lower().strip()

    # Check coin exists
    coin = query_one("SELECT id, symbol, name FROM coins WHERE symbol = %s;", [symbol])
    if not coin:
        return jsonify({"error": f"Coin '{symbol}' not found"}), 404

    # Check duplicate favourite
    existing = query_one(
        "SELECT id FROM favourites WHERE user_id = %s AND coin_id = %s;",
        [user_id, coin["id"]],
    )
    if existing:
        return jsonify({"error": "Coin already in favourites"}), 409

    # Insert favourite (SQLite + PostgreSQL safe)
    execute(
        """
        INSERT INTO favourites (user_id, coin_id)
        VALUES (%s, %s);
        """,
        [user_id, coin["id"]],
    )

    # Fetch inserted row
    new_row = query_one(
        """
        SELECT f.id, c.symbol, c.name, f.added_at
        FROM favourites f
        JOIN coins c ON f.coin_id = c.id
        WHERE f.user_id = %s AND f.coin_id = %s
        ORDER BY f.id DESC
        LIMIT 1;
        """,
        [user_id, coin["id"]],
    )

    return jsonify(new_row), 201


@coins_bp.route("/coins/<int:fav_id>", methods=["PUT"])
def update_favourite(fav_id):
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "Missing or invalid X-User-Id header"}), 400

    data = request.get_json(silent=True)
    if not data or "symbol" not in data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    symbol = data["symbol"].lower().strip()

    # Check favourite exists
    fav = query_one(
        "SELECT id FROM favourites WHERE id = %s AND user_id = %s;",
        [fav_id, user_id],
    )
    if not fav:
        return jsonify({"error": "Favourite not found"}), 404

    # Check coin exists
    coin = query_one("SELECT id, symbol, name FROM coins WHERE symbol = %s;", [symbol])
    if not coin:
        return jsonify({"error": f"Coin '{symbol}' not found"}), 404

    # Update favourite
    execute(
        "UPDATE favourites SET coin_id = %s WHERE id = %s;",
        [coin["id"], fav_id],
    )

    updated = query_one(
        """
        SELECT f.id, c.symbol, c.name, f.added_at
        FROM favourites f
        JOIN coins c ON f.coin_id = c.id
        WHERE f.id = %s;
        """,
        [fav_id],
    )

    return jsonify(updated), 200


# -----------------------------
# DELETE /coins/<id>  (Remove favourite)
# -----------------------------
@coins_bp.route("/coins/<int:fav_id>", methods=["DELETE"])
def delete_favourite(fav_id):
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "Missing or invalid X-User-Id header"}), 400

    deleted = execute(
        "DELETE FROM favourites WHERE id = %s AND user_id = %s;",
        [fav_id, user_id],
    )

    if deleted == 0:
        return jsonify({"error": "Favourite not found"}), 404

    return "", 204

