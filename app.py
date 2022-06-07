from flask import Flask, send_file
from crawler import run_crawler

app = Flask(__name__)

@app.route("/run")
def crawler_endpoint():
    try:
        run_crawler()
        return send_file("/crawler/result.xlsx")
    except Exception as e:
        return str(e)

@app.route("/test")
def test_page():
    return "OK"

app.run(host="0.0.0.0")
