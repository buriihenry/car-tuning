#!/usr/bin/env python3
"""
Web interface for the Car Tuning AI Agent.
Provides a modern web UI and REST API for generating car tuning recommendations.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from pathlib import Path
from dotenv import load_dotenv

from src.main import CarTuningAgent
from src.models import CarInfo, UserPreferences, EngineType, DrivingGoal, BudgetRange, ExperienceLevel

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize the agent with LLM enhancement
agent = CarTuningAgent(use_llm_enhancement=True)

@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')

@app.route('/api/options')
def get_options():
    """Get available options for the system."""
    try:
        options = agent.get_available_options()
        return jsonify({
            'success': True,
            'data': options
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recommendations', methods=['POST'])
def generate_recommendations():
    """Generate tuning recommendations from JSON data."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Generate recommendations
        report = agent.generate_recommendations_from_dict(data)
        
        # Convert to JSON-serializable format using model_dump instead of dict
        report_dict = report.model_dump()
        
        return jsonify({
            'success': True,
            'data': report_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sample')
def get_sample_data():
    """Get sample request data."""
    try:
        sample_data = agent.get_sample_request()
        return jsonify({
            'success': True,
            'data': sample_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/validate', methods=['POST'])
def validate_input():
    """Validate input data."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate car info
        car_info = CarInfo(**data.get('car_info', {}))
        car_valid, car_errors = agent.validator.validate_car_info(car_info)
        
        # Validate user preferences
        user_prefs = UserPreferences(**data.get('user_preferences', {}))
        pref_valid, pref_errors = agent.validator.validate_user_preferences(user_prefs)
        
        # Cross-validation
        complete_valid, cross_errors = agent.validator.validate_complete_request(car_info, user_prefs)
        
        all_errors = car_errors + pref_errors + cross_errors
        
        return jsonify({
            'success': True,
            'data': {
                'valid': len(all_errors) == 0,
                'errors': all_errors,
                'car_valid': car_valid,
                'preferences_valid': pref_valid
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/llm-status')
def get_llm_status():
    """Get LLM enhancement status."""
    try:
        return jsonify({
            'success': True,
            'data': {
                'llm_enabled': agent.use_llm_enhancement,
                'llm_available': agent.llm_enhancer is not None,
                'api_key_configured': bool(os.getenv('GOOGLE_API_KEY'))
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/custom-llm-recommendations', methods=['POST'])
def generate_custom_llm_recommendations():
    """Generate custom recommendations using only the LLM."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        car_info = CarInfo(**data.get('car_info', {}))
        user_preferences = UserPreferences(**data.get('user_preferences', {}))
        
        custom_recommendations = agent.generate_custom_llm_recommendations(car_info, user_preferences)
        
        return jsonify({
            'success': True,
            'data': {
                'recommendations': custom_recommendations
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files."""
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("🚗 Starting Car Tuning AI Agent Web Interface...")
    print("📱 Open your browser to: http://localhost:5000")
    print("🔧 API endpoints available at: http://localhost:5000/api/")
    print(f"🤖 LLM Enhancement: {'Enabled' if agent.use_llm_enhancement else 'Disabled'}")
    
    # Check if API key is configured
    if os.getenv('GOOGLE_API_KEY'):
        print("✅ Google API key found in environment")
    else:
        print("⚠️  No Google API key found. Create a .env file with GOOGLE_API_KEY=your_key")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 