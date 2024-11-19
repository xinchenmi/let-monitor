from flask import Flask, request, jsonify, render_template
from core import ForumMonitor
import json
import threading

app = Flask(__name__)
monitor = ForumMonitor()

# 避免冲突
app.jinja_env.variable_start_string = '<<'
app.jinja_env.variable_end_string = '>>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        data = request.json
        with open('data/config.json', 'w') as f:
            json.dump(data, f, indent=4)
        monitor.reload()
        return jsonify({"status": "success", "message": "Config updated"})
    else:
        return jsonify(monitor.config)

if __name__ == '__main__':
    thread = threading.Thread(target=monitor.start_monitoring)
    thread.daemon = True  # 设置为后台线程，这样主线程退出时它会自动退出
    thread.start()
    app.run(debug=True,host='0.0.0.0',port=5556)
