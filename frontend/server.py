from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Serve static files
@app.route('/')
def index():
    return send_from_directory('static/templates', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    print("🎨 Frontend server starting...")
    print("📱 Open your browser and go to: http://localhost:3000")
    print("🔗 Make sure the backend is running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=3000) 