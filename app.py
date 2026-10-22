from flask import Flask
import time

app = Flask(__name__)

@app.route('/fast')
def fast():
    return "ok"

@app.route('/slow')
def slow():
    time.sleep(0.2)
    return "slow"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)