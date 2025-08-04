"""
Main module for the Car Tuning AI Agent.
Provides the main interface for generating car tuning recommendations.
"""

from typing import Dict, Any, Optional
import json
import os
from datetime import datetime
from dotenv import load_dotenv

from .models import CarInfo, UserPreferences, TuningReport, CarTuningRequest, EngineType, DrivingGoal, BudgetRange, ExperienceLevel
from .recommendation_engine import TuningRecommendationEngine
from .input_validator import InputValidator
from .llm_enhancer import LLMEnhancer

# Load environment variables from .env file
load_dotenv()


class CarTuningAgent:
    """Main agent for generating car tuning recommendations."""
    
    def __init__(self, use_llm_enhancement: bool = True, api_key: Optional[str] = None):
        """Initialize the car tuning agent."""
        self.engine = TuningRecommendationEngine()
        self.validator = InputValidator()
        self.use_llm_enhancement = use_llm_enhancement
        
        # Initialize LLM enhancer if enabled
        self.llm_enhancer = None
        if self.use_llm_enhancement:
            try:
                # Use provided api_key or get from environment
                api_key = api_key or os.getenv('GOOGLE_API_KEY')
                if api_key:
                    self.llm_enhancer = LLMEnhancer(api_key)
                    print("✅ LLM enhancement enabled with Gemini 2.5 Flash")
                else:
                    print("⚠️  LLM enhancement disabled: No Google API key found")
                    print("   Set GOOGLE_API_KEY in your .env file or environment")
                    self.use_llm_enhancement = False
            except Exception as e:
                print(f"⚠️  LLM enhancement disabled: {str(e)}")
                self.use_llm_enhancement = False
    
    def generate_recommendations(self, car_info: CarInfo, user_preferences: UserPreferences) -> TuningReport:
        """Generate tuning recommendations for the given car and preferences."""
        # Validate input
        car_valid, car_errors = self.validator.validate_car_info(car_info)
        pref_valid, pref_errors = self.validator.validate_user_preferences(user_preferences)
        
        if not car_valid or not pref_valid:
            errors = car_errors + pref_errors
            raise ValueError(f"Input validation failed: {'; '.join(errors)}")
        
        # Generate base recommendations
        base_report = self.engine.generate_recommendations(car_info, user_preferences)
        
        # Enhance with LLM if enabled
        if self.use_llm_enhancement and self.llm_enhancer:
            try:
                print("🤖 Enhancing recommendations with Gemini 2.5 Flash...")
                enhanced_report = self.llm_enhancer.enhance_recommendations(base_report)
                return enhanced_report
            except Exception as e:
                print(f"⚠️  LLM enhancement failed, using base recommendations: {str(e)}")
                return base_report
        
        return base_report
    
    def generate_recommendations_from_dict(self, data: Dict[str, Any]) -> TuningReport:
        """Generate recommendations from a dictionary."""
        request = CarTuningRequest(**data)
        return self.generate_recommendations(request.car_info, request.user_preferences)
    
    def generate_recommendations_from_json(self, json_str: str) -> TuningReport:
        """Generate recommendations from a JSON string."""
        data = json.loads(json_str)
        return self.generate_recommendations_from_dict(data)
    
    def export_report_as_json(self, report: TuningReport) -> str:
        """Export the tuning report as a JSON string."""
        return report.model_dump_json(indent=2)
    
    def export_report_as_dict(self, report: TuningReport) -> Dict[str, Any]:
        """Export the tuning report as a dictionary."""
        return report.model_dump()
    
    def get_car_make_suggestions(self, partial_make: str) -> list:
        """Get suggestions for car make based on partial input."""
        return self.validator.get_suggestions_for_make(partial_make)
    
    def get_car_model_suggestions(self, make: str, partial_model: str) -> list:
        """Get suggestions for car model based on partial input."""
        return self.validator.get_suggestions_for_model(make, partial_model)
    
    def get_compatible_engine_types(self, make: str) -> list:
        """Get compatible engine types for a given car make."""
        return self.validator.get_compatible_engine_types(make)
    
    def validate_car_info(self, car_info: CarInfo) -> tuple:
        """Validate car information."""
        return self.validator.validate_car_info(car_info)
    
    def validate_user_preferences(self, user_preferences: UserPreferences) -> tuple:
        """Validate user preferences."""
        return self.validator.validate_user_preferences(user_preferences)
    
    def get_sample_request(self) -> Dict[str, Any]:
        """Get a sample request for testing."""
        return {
            "car_info": {
                "make": "BMW",
                "model": "3 Series",
                "year": 2021,
                "engine_type": "petrol",
                "current_modifications": ["Sport exhaust", "Lowered suspension"]
            },
            "user_preferences": {
                "primary_goals": ["performance", "track_use"],
                "budget_range": "premium",
                "experience_level": "advanced",
                "max_budget": 15000.0
            }
        }
    
    def get_available_options(self) -> Dict[str, Any]:
        """Get all available options for the system."""
        return {
            "engine_types": [et.value for et in EngineType],
            "driving_goals": [goal.value for goal in DrivingGoal],
            "budget_ranges": [br.value for br in BudgetRange],
            "experience_levels": [el.value for el in ExperienceLevel],
            "valid_makes": self.validator.valid_makes,
            "valid_models": self.validator.valid_models,
            "llm_enhancement_enabled": self.use_llm_enhancement
        }
    
    def generate_custom_llm_recommendations(self, car_info: CarInfo, user_preferences: UserPreferences) -> list:
        """Generate custom recommendations using only the LLM."""
        if not self.llm_enhancer:
            raise ValueError("LLM enhancer not available")
        
        return self.llm_enhancer.generate_custom_recommendations(car_info, user_preferences) 