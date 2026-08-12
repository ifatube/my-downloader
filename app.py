from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get-link', methods=['GET'])
def get_link():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # استخراج معرف الفيديو من الرابط
    video_id = video_url.split('v=')[-1].split('&')[0]
    
    # طلب البيانات من خادم Piped (خادم مجاني ومستقر مخصص لفك روابط يوتيوب)
    api_url = f"https://pipedapi.kavin.rocks/streams/{video_id}"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        
        # اختيار أفضل جودة فيديو متاحة
        audio_url = data['audioStreams'][0]['url']
        return jsonify({'url': audio_url, 'title': data['title']})
    except Exception as e:
        return jsonify({'error': "لا يمكن جلب الرابط، قد يكون الفيديو غير متاح عبر هذا الخادم."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
