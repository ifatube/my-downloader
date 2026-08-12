from flask import Flask, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)

@app.route('/get-link', methods=['GET'])
def get_link():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # 1. تحديث yt-dlp أولاً لضمان التعامل مع تحديثات يوتيوب
    # 2. إضافة خيار --no-check-certificate لتجاوز مشاكل الاتصال
    cmd = f"yt-dlp -U && yt-dlp -g --no-check-certificate {video_url}"
    
    try:
        # تنفيذ الأمر
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
        # لأن -g تعطي رابطاً مباشراً، سنأخذ أول رابط في النتائج
        direct_url = result.split('\n')[0]
        return jsonify({'url': direct_url})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f"Command failed: {e.output.decode()}"}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
