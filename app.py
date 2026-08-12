from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get-link', methods=['GET'])
def get_link():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        # استخدام خدمة Invidious API بديلة ومستقرة تماماً
        video_id = video_url.split('v=')[-1].split('&')[0]
        api_url = f"https://invidious.nerdvpn.de/api/v1/videos/{video_id}"
        
        response = requests.get(api_url, timeout=10)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch from primary API'}), 500
            
        data = response.json()
        
        # اختيار أفضل رابط فيديو متاح
        adaptive_formats = data.get('adaptiveFormats', [])
        video_streams = [f for f in adaptive_formats if 'video/mp4' in f.get('type', '')]
        
        if not video_streams:
            return jsonify({'error': 'No video streams found'}), 404
            
        best_stream = video_streams[0]['url']
        return jsonify({'url': best_stream, 'title': data.get('title', '')})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
