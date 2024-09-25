import os
from data.preprocess import main as preprocess_data
from models.fake_news_model import main as train_model
from web.app import app
from social_media.twitter_streamer import start_twitter_stream
from realtime.processor import RealTimeProcessor

def main():
    # Check if processed data exists, if not, preprocess
    if not os.path.exists('data/processed_train.csv'):
        print("Preprocessing data...")
        preprocess_data()
    
    # Train the model
    print("Training the model...")
    train_model()
    
    # Initialize and start the real-time processor
    processor = RealTimeProcessor()
    processor.start()
    
    # Start Twitter stream in a separate thread
    import threading
    twitter_thread = threading.Thread(target=start_twitter_stream, args=('YOUR_BEARER_TOKEN', processor))
    twitter_thread.start()
    
    # Run the Flask app
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    main()