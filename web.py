from flask import Flask, request, jsonify, render_template
from core import ForumMonitor
import json
import threading
import os

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
        data = request.json or {}
        config_payload = data.get('config', {})
        custom_threads = config_payload.get('custom_threads', [])
        sanitized_threads = []
        for thread in custom_threads:
            url = (thread.get('url') or '').strip()
            if not url:
                continue

            sanitized_thread = {
                'url': url,
                'name': (thread.get('name') or '').strip(),
                'use_ai_filter': thread.get('use_ai_filter', True)
            }

            author_value = (thread.get('author') or '').strip()
            if author_value:
                sanitized_thread['author'] = author_value

            if 'monitor_all_authors' in thread:
                sanitized_thread['monitor_all_authors'] = bool(thread.get('monitor_all_authors'))

            sanitized_threads.append(sanitized_thread)

        config_payload['custom_threads'] = sanitized_threads

        os.makedirs('data', exist_ok=True)
        with open('data/config.json', 'w') as f:
            json.dump({'config': config_payload}, f, indent=4)
        monitor.reload()
        return jsonify({"status": "success", "message": "Config updated"})
    else:
        return jsonify(monitor.config)

if __name__ == '__main__':
    thread = threading.Thread(target=monitor.start_monitoring)
    thread.daemon = True  # 设置为后台线程，这样主线程退出时它会自动退出
    thread.start()
    app.run(debug=True, host='0.0.0.0', port=5556)
