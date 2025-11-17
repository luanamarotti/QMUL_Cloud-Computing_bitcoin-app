from flask import Flask
from external_api import external_api_bp  # imports the blueprint with external API routes

def create_app():
    app = Flask(__name__)

    # register external API blueprint
    app.register_blueprint(external_api_bp)

    @app.route("/")
    def index():
        return {"message": "Bitcoin app is running!"}

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
