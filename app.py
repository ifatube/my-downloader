from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/get-link', methods=['GET'])
def get_link():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    # نستخدم yt-dlp لجلب الرابط المباشر
    cmd = f"yt-dlp -g {video_url}"
    try:
        # تنفيذ الأمر واستقبال الرابط
        result = subprocess.check_output(cmd, shell=True).decode().strip()
        return jsonify({'url': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))