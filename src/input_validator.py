"""
Input validation module for car tuning AI agent.
Ensures data integrity and provides helpful error messages.
"""

from typing import List, Dict, Any, Optional, Tuple
from .models import (
    CarInfo, UserPreferences, EngineType, DrivingGoal, 
    BudgetRange, ExperienceLevel
)


class InputValidator:
    """Validates user input for car tuning requests."""
    
    def __init__(self):
        self.valid_makes = self._get_valid_makes()
        self.valid_models = self._get_valid_models()
        self.engine_compatibility = self._get_engine_compatibility()
    
    def _get_valid_makes(self) -> List[str]:
        """Get list of valid car makes."""
        return [
            "Toyota", "Honda", "Ford", "Chevrolet", "Nissan", "BMW", "Mercedes-Benz",
            "Audi", "Volkswagen", "Hyundai", "Kia", "Mazda", "Subaru", "Mitsubishi",
            "Lexus", "Infiniti", "Acura", "Volvo", "Saab", "Peugeot", "Renault",
            "Fiat", "Alfa Romeo", "Ferrari", "Lamborghini", "Porsche", "Aston Martin",
            "Bentley", "Rolls-Royce", "McLaren", "Bugatti", "Koenigsegg", "Pagani",
            "Tesla", "Rivian", "Lucid", "Polestar", "NIO", "BYD", "Rimac"
        ]
    
    def _get_valid_models(self) -> Dict[str, List[str]]:
        """Get valid models for each make."""
        return {
            "Toyota": ["Camry", "Corolla", "Prius", "RAV4", "Highlander", "Tacoma", "Tundra", "Supra", "86"],
            "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Ridgeline", "NSX", "S2000"],
            "Ford": ["F-150", "Mustang", "Focus", "Fusion", "Escape", "Explorer", "Bronco", "GT"],
            "BMW": ["3 Series", "5 Series", "7 Series", "X3", "X5", "M3", "M5", "i3", "i8"],
            "Mercedes-Benz": ["C-Class", "E-Class", "S-Class", "GLC", "GLE", "AMG GT", "EQS"],
            "Audi": ["A3", "A4", "A6", "Q3", "Q5", "Q7", "RS3", "RS6", "e-tron"],
            "Tesla": ["Model S", "Model 3", "Model X", "Model Y", "Cybertruck", "Roadster"],
            "Porsche": ["911", "Cayman", "Boxster", "Cayenne", "Macan", "Panamera", "Taycan"]
        }
    
    def _get_engine_compatibility(self) -> Dict[EngineType, List[str]]:
        """Get engine type compatibility with different vehicle types."""
        return {
            EngineType.PETROL: ["Toyota", "Honda", "Ford", "BMW", "Mercedes-Benz", "Audi", "Porsche"],
            EngineType.DIESEL: ["BMW", "Mercedes-Benz", "Audi", "Volkswagen", "Volvo"],
            EngineType.HYBRID: ["Toyota", "Honda", "Ford", "BMW", "Mercedes-Benz", "Audi"],
            EngineType.ELECTRIC: ["Tesla", "BMW", "Mercedes-Benz", "Audi", "Porsche", "Rivian", "Lucid"]
        }
    
    def validate_car_info(self, car_info: CarInfo) -> Tuple[bool, List[str]]:
        """Validate car information."""
        errors = []
        
        # Validate make
        if not self._validate_make(car_info.make):
            errors.append(f"Invalid car make: {car_info.make}")
        
        # Validate model
        if not self._validate_model(car_info.make, car_info.model):
            errors.append(f"Invalid model '{car_info.model}' for make '{car_info.make}'")
        
        # Validate year
        if not self._validate_year(car_info.year):
            errors.append(f"Invalid year: {car_info.year}. Must be between 1900 and 2030")
        
        # Validate engine type compatibility - make this less restrictive
        if not self._validate_engine_compatibility(car_info.make, car_info.engine_type):
            # Only warn for unusual combinations, don't fail validation
            errors.append(f"Warning: Engine type '{car_info.engine_type.value}' may not be typical for {car_info.make}")
        
        # Validate current modifications
        if car_info.current_modifications:
            for mod in car_info.current_modifications:
                if not self._validate_modification(mod):
                    errors.append(f"Invalid modification: {mod}")
        
        return len(errors) == 0, errors
    
    def validate_user_preferences(self, preferences: UserPreferences) -> Tuple[bool, List[str]]:
        """Validate user preferences."""
        errors = []
        
        # Validate primary goals
        if not preferences.primary_goals:
            errors.append("At least one primary goal must be specified")
        else:
            for goal in preferences.primary_goals:
                if not self._validate_goal(goal):
                    errors.append(f"Invalid driving goal: {goal.value}")
        
        # Validate budget range
        if not self._validate_budget_range(preferences.budget_range):
            errors.append(f"Invalid budget range: {preferences.budget_range.value}")
        
        # Validate experience level
        if not self._validate_experience_level(preferences.experience_level):
            errors.append(f"Invalid experience level: {preferences.experience_level.value}")
        
        # Validate max budget if provided
        if preferences.max_budget is not None:
            if not self._validate_max_budget(preferences.max_budget, preferences.budget_range):
                errors.append(f"Max budget ${preferences.max_budget} is outside the specified budget range")
        
        return len(errors) == 0, errors
    
    def _validate_make(self, make: str) -> bool:
        """Validate car make."""
        # Make validation case-insensitive
        make_lower = make.lower()
        valid_makes_lower = [valid_make.lower() for valid_make in self.valid_makes]
        return make_lower in valid_makes_lower
    
    def _validate_model(self, make: str, model: str) -> bool:
        """Validate car model for the given make."""
        if make not in self.valid_models:
            return True  # If make not in our list, we can't validate model
        
        return model in self.valid_models[make]
    
    def _validate_year(self, year: int) -> bool:
        """Validate car year."""
        return 1900 <= year <= 2030
    
    def _validate_engine_compatibility(self, make: str, engine_type: EngineType) -> bool:
        """Validate engine type compatibility with car make."""
        # For common makes, be more permissive
        common_makes = ["Toyota", "Honda", "Ford", "BMW", "Mercedes-Benz", "Audi", "Volkswagen", "Hyundai", "Kia"]
        common_makes_lower = [m.lower() for m in common_makes]
        if make.lower() in common_makes_lower:
            return True  # Allow common makes with any engine type
        
        # For specific makes, check compatibility
        compatible_makes = self.engine_compatibility.get(engine_type, [])
        compatible_makes_lower = [m.lower() for m in compatible_makes]
        return make.lower() in compatible_makes_lower
    
    def _validate_modification(self, modification: str) -> bool:
        """Validate current modification description."""
        # Basic validation - check for reasonable length and content
        if len(modification) < 3 or len(modification) > 100:
            return False
        
        # Check for potentially inappropriate content
        inappropriate_words = ["illegal", "unsafe", "dangerous", "void"]
        if any(word in modification.lower() for word in inappropriate_words):
            return False
        
        return True
    
    def _validate_goal(self, goal: DrivingGoal) -> bool:
        """Validate driving goal."""
        return goal in DrivingGoal
    
    def _validate_budget_range(self, budget_range: BudgetRange) -> bool:
        """Validate budget range."""
        return budget_range in BudgetRange
    
    def _validate_experience_level(self, experience_level: ExperienceLevel) -> bool:
        """Validate experience level."""
        return experience_level in ExperienceLevel
    
    def _validate_max_budget(self, max_budget: float, budget_range: BudgetRange) -> bool:
        """Validate max budget against budget range."""
        budget_ranges = {
            BudgetRange.BUDGET: (500, 2000),
            BudgetRange.MODERATE: (2000, 8000),
            BudgetRange.PREMIUM: (8000, 20000),
            BudgetRange.UNLIMITED: (20000, 100000)
        }
        
        min_budget, max_budget_range = budget_ranges.get(budget_range, (0, 0))
        return min_budget <= max_budget <= max_budget_range
    
    def get_suggestions_for_make(self, partial_make: str) -> List[str]:
        """Get suggestions for car make based on partial input."""
        suggestions = []
        partial_lower = partial_make.lower()
        
        for make in self.valid_makes:
            if partial_lower in make.lower():
                suggestions.append(make)
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def get_suggestions_for_model(self, make: str, partial_model: str) -> List[str]:
        """Get suggestions for car model based on partial input."""
        if make not in self.valid_models:
            return []
        
        suggestions = []
        partial_lower = partial_model.lower()
        
        for model in self.valid_models[make]:
            if partial_lower in model.lower():
                suggestions.append(model)
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def get_compatible_engine_types(self, make: str) -> List[EngineType]:
        """Get compatible engine types for a given car make."""
        compatible_types = []
        
        for engine_type, makes in self.engine_compatibility.items():
            if make in makes:
                compatible_types.append(engine_type)
        
        return compatible_types
    
    def validate_complete_request(self, car_info: CarInfo, user_preferences: UserPreferences) -> Tuple[bool, List[str]]:
        """Validate complete tuning request."""
        car_valid, car_errors = self.validate_car_info(car_info)
        pref_valid, pref_errors = self.validate_user_preferences(user_preferences)
        
        all_errors = car_errors + pref_errors
        
        # Additional cross-validation
        if car_valid and pref_valid:
            cross_errors = self._cross_validate(car_info, user_preferences)
            all_errors.extend(cross_errors)
        
        return len(all_errors) == 0, all_errors
    
    def _cross_validate(self, car_info: CarInfo, user_preferences: UserPreferences) -> List[str]:
        """Cross-validate car info and user preferences."""
        errors = []
        
        # Check if electric vehicle goals are appropriate
        if car_info.engine_type == EngineType.ELECTRIC:
            if DrivingGoal.FUEL_ECONOMY in user_preferences.primary_goals:
                errors.append("Fuel economy goal is not applicable for electric vehicles")
            
            if DrivingGoal.TRACK_USE in user_preferences.primary_goals:
                errors.append("Track use modifications for electric vehicles may have limited options")
        
        # Check if budget is appropriate for the car make
        if user_preferences.budget_range == BudgetRange.BUDGET:
            luxury_makes = ["BMW", "Mercedes-Benz", "Audi", "Porsche", "Ferrari", "Lamborghini"]
            if car_info.make in luxury_makes:
                errors.append("Budget range may be too low for luxury vehicle modifications")
        
        # Check experience level vs modification complexity
        if user_preferences.experience_level == ExperienceLevel.BEGINNER:
            if DrivingGoal.TRACK_USE in user_preferences.primary_goals:
                errors.append("Track use modifications may be too complex for beginners")
        
        return errors 