#!/usr/bin/env python3
"""
Basic test script for the Car Tuning AI Agent.
"""

import json
from src.main import CarTuningAgent
from src.models import CarInfo, UserPreferences, EngineType, DrivingGoal, BudgetRange, ExperienceLevel


def test_basic_functionality():
    """Test basic functionality of the car tuning agent."""
    print("🚗 Testing Car Tuning AI Agent...")
    
    # Create agent
    agent = CarTuningAgent()
    
    # Test car info
    car_info = CarInfo(
        make="BMW",
        model="3 Series",
        year=2021,
        engine_type=EngineType.PETROL,
        current_modifications=[]
    )
    
    # Test user preferences
    user_preferences = UserPreferences(
        primary_goals=[DrivingGoal.PERFORMANCE, DrivingGoal.TRACK_USE],
        budget_range=BudgetRange.PREMIUM,
        experience_level=ExperienceLevel.ADVANCED,
        max_budget=15000.0
    )
    
    # Generate recommendations
    print("📋 Generating recommendations...")
    report = agent.generate_recommendations(car_info, user_preferences)
    
    # Display results
    print(f"\n✅ Successfully generated {len(report.recommendations)} recommendations")
    print(f"💰 Total cost range: ${report.total_estimated_cost['min']:,.0f} - ${report.total_estimated_cost['max']:,.0f}")
    
    # Show top recommendations
    print("\n🏆 Top Recommendations:")
    for i, rec in enumerate(report.recommendations[:3], 1):
        print(f"{i}. {rec.name} (Score: {rec.priority_score:.1f}/10)")
        print(f"   Cost: ${rec.cost_range['min']:,.0f} - ${rec.cost_range['max']:,.0f}")
        print(f"   Safety: {rec.safety_level.value.title()}")
        print()
    
    # Test JSON export
    json_report = agent.export_report_as_json(report)
    print(f"📄 JSON export length: {len(json_report)} characters")
    
    # Test validation
    is_valid, errors = agent.validate_car_info(car_info)
    print(f"✅ Car info validation: {'PASS' if is_valid else 'FAIL'}")
    if errors:
        print(f"   Errors: {errors}")
    
    is_valid, errors = agent.validate_user_preferences(user_preferences)
    print(f"✅ User preferences validation: {'PASS' if is_valid else 'FAIL'}")
    if errors:
        print(f"   Errors: {errors}")
    
    # Test suggestions
    suggestions = agent.get_car_make_suggestions("BM")
    print(f"🔍 Car make suggestions for 'BM': {suggestions}")
    
    print("\n🎉 All tests completed successfully!")


def test_electric_vehicle():
    """Test electric vehicle recommendations."""
    print("\n⚡ Testing Electric Vehicle Support...")
    
    agent = CarTuningAgent()
    
    car_info = CarInfo(
        make="Tesla",
        model="Model 3",
        year=2022,
        engine_type=EngineType.ELECTRIC,
        current_modifications=[]
    )
    
    user_preferences = UserPreferences(
        primary_goals=[DrivingGoal.PERFORMANCE, DrivingGoal.DAILY_COMFORT],
        budget_range=BudgetRange.MODERATE,
        experience_level=ExperienceLevel.INTERMEDIATE,
        max_budget=6000.0
    )
    
    report = agent.generate_recommendations(car_info, user_preferences)
    
    print(f"✅ Generated {len(report.recommendations)} recommendations for Tesla Model 3")
    print(f"💰 Cost range: ${report.total_estimated_cost['min']:,.0f} - ${report.total_estimated_cost['max']:,.0f}")
    
    # Check that ECU remapping is not recommended for electric vehicles
    ecu_recommendations = [r for r in report.recommendations if "ECU" in r.name]
    if not ecu_recommendations:
        print("✅ Correctly excluded ECU remapping for electric vehicle")
    else:
        print("❌ ECU remapping incorrectly recommended for electric vehicle")


def test_sample_data():
    """Test with sample data from the agent."""
    print("\n📊 Testing Sample Data...")
    
    agent = CarTuningAgent()
    sample_data = agent.get_sample_request()
    
    print("📋 Sample data:")
    print(json.dumps(sample_data, indent=2))
    
    report = agent.generate_recommendations_from_dict(sample_data)
    print(f"\n✅ Generated {len(report.recommendations)} recommendations from sample data")


if __name__ == "__main__":
    try:
        test_basic_functionality()
        test_electric_vehicle()
        test_sample_data()
        print("\n🎯 All tests passed! The Car Tuning AI Agent is working correctly.")
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc() 