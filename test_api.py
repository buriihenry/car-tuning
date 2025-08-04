#!/usr/bin/env python3
"""
Simple API test script for the Car Tuning AI Agent.
"""

from src.main import CarTuningAgent
from src.models import CarInfo, UserPreferences, EngineType, DrivingGoal, BudgetRange, ExperienceLevel


def test_api():
    """Test the API functionality."""
    print("🚗 Testing Car Tuning AI Agent API...")
    
    # Create agent
    agent = CarTuningAgent()
    
    # Test different scenarios
    scenarios = [
        {
            "name": "BMW Performance",
            "car_info": CarInfo(
                make="BMW",
                model="3 Series",
                year=2021,
                engine_type=EngineType.PETROL,
                current_modifications=[]
            ),
            "user_preferences": UserPreferences(
                primary_goals=[DrivingGoal.PERFORMANCE, DrivingGoal.TRACK_USE],
                budget_range=BudgetRange.PREMIUM,
                experience_level=ExperienceLevel.ADVANCED,
                max_budget=15000.0
            )
        },
        {
            "name": "Tesla Electric",
            "car_info": CarInfo(
                make="Tesla",
                model="Model 3",
                year=2022,
                engine_type=EngineType.ELECTRIC,
                current_modifications=[]
            ),
            "user_preferences": UserPreferences(
                primary_goals=[DrivingGoal.PERFORMANCE, DrivingGoal.DAILY_COMFORT],
                budget_range=BudgetRange.MODERATE,
                experience_level=ExperienceLevel.INTERMEDIATE,
                max_budget=6000.0
            )
        },
        {
            "name": "Toyota Beginner",
            "car_info": CarInfo(
                make="Toyota",
                model="Camry",
                year=2020,
                engine_type=EngineType.PETROL,
                current_modifications=[]
            ),
            "user_preferences": UserPreferences(
                primary_goals=[DrivingGoal.DAILY_COMFORT, DrivingGoal.FUEL_ECONOMY],
                budget_range=BudgetRange.BUDGET,
                experience_level=ExperienceLevel.BEGINNER,
                max_budget=2000.0
            )
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 Testing: {scenario['name']}")
        print(f"   Vehicle: {scenario['car_info'].year} {scenario['car_info'].make} {scenario['car_info'].model}")
        print(f"   Engine: {scenario['car_info'].engine_type.value}")
        print(f"   Goals: {[g.value for g in scenario['user_preferences'].primary_goals]}")
        print(f"   Budget: {scenario['user_preferences'].budget_range.value}")
        print(f"   Experience: {scenario['user_preferences'].experience_level.value}")
        
        # Generate recommendations
        report = agent.generate_recommendations(scenario['car_info'], scenario['user_preferences'])
        
        print(f"   ✅ Generated {len(report.recommendations)} recommendations")
        print(f"   💰 Cost range: ${report.total_estimated_cost['min']:,.0f} - ${report.total_estimated_cost['max']:,.0f}")
        
        # Show top recommendation
        if report.recommendations:
            top_rec = report.recommendations[0]
            print(f"   🏆 Top recommendation: {top_rec.name} (Score: {top_rec.priority_score:.1f}/10)")
        
        print()
    
    print("🎉 All API tests completed successfully!")


if __name__ == "__main__":
    test_api() 