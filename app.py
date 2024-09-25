from flask import Flask, render_template, request, jsonify
from realtime.processor import RealTimeProcessor

app = Flask(__name__)
processor = RealTimeProcessor()
processor.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    article_text = request.form['article_text']
    source_url = request.form['source_url']
    
    processor.add_article(article_text, source_url)
    
    # In a real application, you'd want to wait for the result
    # Here we're just returning a placeholder
    return jsonify({'status': 'Processing', 'queue_size': processor.get_queue_size()})

@app.route('/status')
def status():
    return jsonify({'queue_size': processor.get_queue_size()})

if __name__ == '__main__':
    app.run(debug=True)