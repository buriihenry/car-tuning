#!/usr/bin/env python3
"""
Test script for LLM integration with Gemini 2.5 Flash.
"""

import os
import json
from src.main import CarTuningAgent
from src.models import CarInfo, UserPreferences, EngineType, DrivingGoal, BudgetRange, ExperienceLevel

def test_llm_integration():
    """Test LLM integration with Gemini 2.5 Flash."""
    print("🤖 Testing LLM Integration with Gemini 2.5 Flash...")
    
    # Check if API key is available
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("⚠️  No GOOGLE_API_KEY environment variable found.")
        print("   To test LLM integration, set your Google API key:")
        print("   export GOOGLE_API_KEY='your-api-key-here'")
        print("\n   For now, testing without LLM enhancement...")
        use_llm = False
    else:
        print("✅ Google API key found")
        use_llm = True
    
    try:
        # Initialize agent
        agent = CarTuningAgent(use_llm_enhancement=use_llm, api_key=api_key)
        
        # Test data
        car_info = CarInfo(
            make="BMW",
            model="3 Series",
            year=2021,
            engine_type=EngineType.PETROL,
            current_modifications=["Sport exhaust"]
        )
        
        user_preferences = UserPreferences(
            primary_goals=[DrivingGoal.PERFORMANCE, DrivingGoal.TRACK_USE],
            budget_range=BudgetRange.PREMIUM,
            experience_level=ExperienceLevel.ADVANCED,
            max_budget=15000.0
        )
        
        print(f"\n📋 Test Configuration:")
        print(f"   Car: {car_info.year} {car_info.make} {car_info.model}")
        print(f"   Engine: {car_info.engine_type.value}")
        print(f"   Goals: {[g.value for g in user_preferences.primary_goals]}")
        print(f"   Budget: {user_preferences.budget_range.value}")
        print(f"   Experience: {user_preferences.experience_level.value}")
        print(f"   LLM Enhancement: {'Enabled' if use_llm else 'Disabled'}")
        
        # Generate recommendations
        print(f"\n🔄 Generating recommendations...")
        report = agent.generate_recommendations(car_info, user_preferences)
        
        print(f"✅ Generated {len(report.recommendations)} recommendations")
        print(f"💰 Total cost range: ${report.total_estimated_cost['min']:,.0f} - ${report.total_estimated_cost['max']:,.0f}")
        
        # Show enhanced features if LLM is enabled
        if use_llm and agent.llm_enhancer:
            print(f"\n🤖 LLM-Enhanced Features:")
            print(f"   - Enhanced descriptions with technical details")
            print(f"   - Additional benefits and considerations")
            print(f"   - Improved safety warnings")
            print(f"   - Installation tips and maintenance advice")
            print(f"   - Overall analysis and professional advice")
            
            # Test custom LLM recommendations
            print(f"\n🧠 Testing custom LLM recommendations...")
            custom_recs = agent.generate_custom_llm_recommendations(car_info, user_preferences)
            print(f"✅ Generated {len(custom_recs)} custom LLM recommendations")
            
            # Show a sample custom recommendation
            if custom_recs:
                sample = custom_recs[0]
                print(f"\n📝 Sample Custom Recommendation:")
                print(f"   Name: {sample.get('name', 'N/A')}")
                print(f"   Category: {sample.get('category', 'N/A')}")
                print(f"   Cost: ${sample.get('cost_range', {}).get('min', 0):,.0f} - ${sample.get('cost_range', {}).get('max', 0):,.0f}")
                print(f"   Safety Level: {sample.get('safety_level', 'N/A')}")
        
        # Export to JSON
        json_output = agent.export_report_as_json(report)
        print(f"\n📄 Report exported as JSON ({len(json_output)} characters)")
        
        # Save to file
        with open('llm_test_report.json', 'w') as f:
            f.write(json_output)
        print(f"💾 Report saved to 'llm_test_report.json'")
        
        print(f"\n🎉 LLM integration test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during LLM integration test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_llm_integration() 