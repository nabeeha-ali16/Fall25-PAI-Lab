import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

api_key = "syaM1VXzEULInEaHrbLu7SUTTbEllZRHPUJA10c9"
url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"


@app.route("/")
def main():
    try:
        response = requests.get(url)

        if response.status_code == 200:
            nasa_data = response.json()
            return render_template("index.html", data=nasa_data)

        else:
            return {"error": "Unable to fetch NASA data"}

    except Exception as e:
        return {"error": str(e)}


@app.route("/api/nasa")
def nasa_api():
    try:
        response = requests.get(url)
        data = response.json()
        return jsonify(data)

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    app.run(debug=True)  
