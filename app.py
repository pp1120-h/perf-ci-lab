from flask import Flask
import time

app = Flask(__name__)

@app.route('/fast')
def fast():
    time.sleep(0.5)  # 故意让它慢 500ms，突破 300ms 的底线
    return "ok"

@app.route('/slow')
def slow():
    time.sleep(0.2)
    return "slow"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)