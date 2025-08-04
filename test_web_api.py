#!/usr/bin/env python3
"""
Test script for the web API endpoints.
"""

import requests
import json
import time

def test_web_api():
    """Test the web API endpoints."""
    base_url = "http://localhost:5000"
    
    print("🚗 Testing Car Tuning AI Agent Web API...")
    
    # Wait a moment for the server to start
    time.sleep(2)
    
    try:
        # Test 1: Get options
        print("\n📋 Testing /api/options...")
        response = requests.get(f"{base_url}/api/options")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✅ Options endpoint working")
                print(f"   Engine types: {len(data['data']['engine_types'])}")
                print(f"   Driving goals: {len(data['data']['driving_goals'])}")
                print(f"   Supported makes: {len(data['data']['valid_makes'])}")
            else:
                print("❌ Options endpoint failed")
        else:
            print(f"❌ Options endpoint returned status {response.status_code}")
        
        # Test 2: Get sample data
        print("\n📋 Testing /api/sample...")
        response = requests.get(f"{base_url}/api/sample")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✅ Sample endpoint working")
                sample = data['data']
                print(f"   Sample car: {sample['car_info']['year']} {sample['car_info']['make']} {sample['car_info']['model']}")
                print(f"   Goals: {sample['user_preferences']['primary_goals']}")
            else:
                print("❌ Sample endpoint failed")
        else:
            print(f"❌ Sample endpoint returned status {response.status_code}")
        
        # Test 3: Generate recommendations
        print("\n📋 Testing /api/recommendations...")
        test_data = {
            "car_info": {
                "make": "BMW",
                "model": "3 Series",
                "year": 2021,
                "engine_type": "petrol",
                "current_modifications": []
            },
            "user_preferences": {
                "primary_goals": ["performance", "track_use"],
                "budget_range": "premium",
                "experience_level": "advanced",
                "max_budget": 15000.0
            }
        }
        
        response = requests.post(
            f"{base_url}/api/recommendations",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✅ Recommendations endpoint working")
                report = data['data']
                print(f"   Generated {len(report['recommendations'])} recommendations")
                print(f"   Cost range: ${report['total_estimated_cost']['min']:,.0f} - ${report['total_estimated_cost']['max']:,.0f}")
            else:
                print("❌ Recommendations endpoint failed")
        else:
            print(f"❌ Recommendations endpoint returned status {response.status_code}")
        
        # Test 4: Validate input
        print("\n📋 Testing /api/validate...")
        response = requests.post(
            f"{base_url}/api/validate",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✅ Validation endpoint working")
                validation = data['data']
                print(f"   Valid: {validation['valid']}")
                if validation['errors']:
                    print(f"   Errors: {validation['errors']}")
            else:
                print("❌ Validation endpoint failed")
        else:
            print(f"❌ Validation endpoint returned status {response.status_code}")
        
        print("\n🎉 All web API tests completed!")
        print(f"🌐 Web interface available at: {base_url}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to web server. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error testing web API: {str(e)}")

if __name__ == "__main__":
    test_web_api() 