from flask import Flask


if __name__ == "__main__":
    app = Flask(__name__)

    import personapi

    app.run(host='0.0.0.0', port=5000)