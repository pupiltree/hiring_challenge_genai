from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import the AdGenerator and analytics service
from services.ad_service import AdGenerator
from services.analytics_service import track_event, get_analytics

load_dotenv()

app = Flask(__name__)
CORS(app) # Enable CORS for frontend interaction

ad_generator = AdGenerator()

@app.route('/api/generate', methods=['POST'])
def generate_ads():
    data = request.json
    if not data:
        return jsonify({'message': 'Invalid input'}), 400

    try:
        # Basic input validation
        required_fields = ['productName', 'description', 'audience']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'message': f'Missing required field: {field}'}), 400

        images = ad_generator.generate_image_ads(data)
        video = ad_generator.generate_video_ad(data)

        # In a real app, you might save results to a DB and return IDs/URLs
        # For this demo, returning placeholder structures with dummy URLs
        # NOTE: Replace with actual URLs from AI model outputs
        results = {
            'images': [{'url': img_url} for img_url in images],
            'video': {'url': video}
        }
        
        # Track the ad generation event
        track_event('generation', 'new_ad_batch') 

        return jsonify(results)

    except Exception as e:
        app.logger.error(f"Error generating ads: {e}")
        return jsonify({'message': 'Internal server error during ad generation'}), 500

# Route to get analytics data
@app.route('/api/analytics', methods=['GET'])
def get_analytics_data():
    data = get_analytics()
    return jsonify(data)

# New route to handle A/B test selections
@app.route('/api/ab-test', methods=['POST'])
def track_ab_test():
    data = request.json
    if not data or 'selectedOption' not in data:
        return jsonify({'message': 'Invalid input: missing selectedOption'}), 400

    try:
        selected_option = data['selectedOption']
        # Track the A/B test selection event
        track_event('ab_test_selection', selected_option)
        return jsonify({'message': 'A/B test selection tracked successfully'})
    except Exception as e:
        app.logger.error(f"Error tracking A/B test: {e}")
        return jsonify({'message': 'Internal server error tracking A/B test'}), 500

if __name__ == '__main__':
    # In a production Docker environment, a web server like Gunicorn would run the app
    # For local testing, you can run this directly
    app.run(host='0.0.0.0', port=5000, debug=True) 