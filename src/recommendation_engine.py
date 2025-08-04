"""
Core recommendation engine for car tuning suggestions.
Processes user input and generates personalized recommendations.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from .models import (
    CarInfo, UserPreferences, TuningRecommendation, TuningReport,
    TuningCategory, DrivingGoal, BudgetRange, ExperienceLevel,
    EngineType, SafetyLevel
)
from .knowledge_base import TuningKnowledgeBase


class TuningRecommendationEngine:
    """Main engine for generating car tuning recommendations."""
    
    def __init__(self):
        self.knowledge_base = TuningKnowledgeBase()
        self.goal_priorities = self._initialize_goal_priorities()
        self.experience_filters = self._initialize_experience_filters()
    
    def _initialize_goal_priorities(self) -> Dict[DrivingGoal, List[TuningCategory]]:
        """Initialize priority categories for each driving goal."""
        return {
            DrivingGoal.PERFORMANCE: [
                TuningCategory.ECU_REMAPPING,
                TuningCategory.EXHAUST_SYSTEM,
                TuningCategory.AIR_INTAKE,
                TuningCategory.TIRES_WHEELS,
                TuningCategory.BRAKE_SYSTEM,
                TuningCategory.SUSPENSION,
                TuningCategory.COSMETIC
            ],
            DrivingGoal.FUEL_ECONOMY: [
                TuningCategory.ECU_REMAPPING,
                TuningCategory.AIR_INTAKE,
                TuningCategory.TIRES_WHEELS,
                TuningCategory.COSMETIC
            ],
            DrivingGoal.DAILY_COMFORT: [
                TuningCategory.SUSPENSION,
                TuningCategory.TIRES_WHEELS,
                TuningCategory.COSMETIC
            ],
            DrivingGoal.TRACK_USE: [
                TuningCategory.ECU_REMAPPING,
                TuningCategory.BRAKE_SYSTEM,
                TuningCategory.SUSPENSION,
                TuningCategory.TIRES_WHEELS,
                TuningCategory.EXHAUST_SYSTEM,
                TuningCategory.AIR_INTAKE,
                TuningCategory.COSMETIC
            ],
            DrivingGoal.OFF_ROADING: [
                TuningCategory.SUSPENSION,
                TuningCategory.TIRES_WHEELS,
                TuningCategory.BRAKE_SYSTEM,
                TuningCategory.COSMETIC
            ]
        }
    
    def _initialize_experience_filters(self) -> Dict[ExperienceLevel, Dict[str, Any]]:
        """Initialize experience-based filters for recommendations."""
        return {
            ExperienceLevel.BEGINNER: {
                "max_safety_level": SafetyLevel.MEDIUM,
                "max_priority_score": 7.0,
                "prefer_professional_installation": True,
                "avoid_high_risk_mods": True
            },
            ExperienceLevel.INTERMEDIATE: {
                "max_safety_level": SafetyLevel.HIGH,
                "max_priority_score": 8.5,
                "prefer_professional_installation": False,
                "avoid_high_risk_mods": False
            },
            ExperienceLevel.ADVANCED: {
                "max_safety_level": SafetyLevel.HIGH,
                "max_priority_score": 10.0,
                "prefer_professional_installation": False,
                "avoid_high_risk_mods": False
            }
        }
    
    def generate_recommendations(self, car_info: CarInfo, user_preferences: UserPreferences) -> TuningReport:
        """Generate comprehensive tuning recommendations."""
        # Get budget constraints
        budget_range = self.knowledge_base.get_budget_range(user_preferences.budget_range)
        max_budget = user_preferences.max_budget or budget_range["max"]
        
        # Get experience filters
        experience_filters = self.experience_filters[user_preferences.experience_level]
        
        # Generate recommendations for each goal
        all_recommendations = []
        for goal in user_preferences.primary_goals:
            goal_recommendations = self._generate_goal_recommendations(
                car_info, user_preferences, goal, max_budget, experience_filters
            )
            all_recommendations.extend(goal_recommendations)
        
        # Remove duplicates and sort by priority
        unique_recommendations = self._deduplicate_recommendations(all_recommendations)
        sorted_recommendations = sorted(unique_recommendations, key=lambda x: x.priority_score, reverse=True)
        
        # Filter by budget and limit recommendations
        filtered_recommendations = self._filter_by_budget(sorted_recommendations, max_budget)
        
        # Calculate total costs
        total_cost = self._calculate_total_cost(filtered_recommendations)
        
        # Generate compatibility matrix
        compatibility_matrix = self._generate_compatibility_matrix(filtered_recommendations)
        
        # Generate safety and legal summaries
        safety_summary = self._generate_safety_summary(filtered_recommendations)
        legal_summary = self._generate_legal_summary(filtered_recommendations)
        
        # Create disclaimer
        disclaimer = self._generate_disclaimer(car_info, user_preferences)
        
        return TuningReport(
            car_info=car_info,
            user_preferences=user_preferences,
            recommendations=filtered_recommendations,
            total_estimated_cost=total_cost,
            compatibility_matrix=compatibility_matrix,
            safety_summary=safety_summary,
            legal_summary=legal_summary,
            disclaimer=disclaimer,
            generated_at=datetime.now().isoformat()
        )
    
    def _generate_goal_recommendations(
        self, 
        car_info: CarInfo, 
        user_preferences: UserPreferences, 
        goal: DrivingGoal, 
        max_budget: float,
        experience_filters: Dict[str, Any]
    ) -> List[TuningRecommendation]:
        """Generate recommendations for a specific driving goal."""
        recommendations = []
        priority_categories = self.goal_priorities[goal]
        
        for category in priority_categories:
            category_options = self.knowledge_base.get_tuning_options_for_category(category)
            
            for option in category_options:
                # Apply experience filters
                if not self._passes_experience_filters(option, experience_filters):
                    continue
                
                # Apply budget filter
                if option["cost_range"]["max"] > max_budget:
                    continue
                
                # Apply engine type compatibility
                if not self._is_compatible_with_engine(option, car_info.engine_type):
                    continue
                
                # Create recommendation
                recommendation = TuningRecommendation(
                    category=category,
                    name=option["name"],
                    description=option["description"],
                    benefits=option["benefits"],
                    cost_range=option["cost_range"],
                    compatibility_notes=option["compatibility_notes"],
                    prerequisites=option["prerequisites"],
                    safety_warnings=option["safety_warnings"],
                    legal_considerations=option["legal_considerations"],
                    warranty_impact=option["warranty_impact"],
                    emissions_impact=option["emissions_impact"],
                    insurance_impact=option["insurance_impact"],
                    priority_score=option["priority_score"],
                    safety_level=option["safety_level"],
                    installation_difficulty=option["installation_difficulty"],
                    professional_required=option["professional_required"]
                )
                
                # Adjust priority score based on goals
                adjusted_score = self._adjust_priority_score(recommendation, goal, user_preferences)
                recommendation.priority_score = adjusted_score
                
                recommendations.append(recommendation)
        
        return recommendations
    
    def _passes_experience_filters(self, option: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Check if an option passes experience-based filters."""
        # Check safety level
        if option["safety_level"].value > filters["max_safety_level"].value:
            return False
        
        # Check priority score
        if option["priority_score"] > filters["max_priority_score"]:
            return False
        
        # Check if high-risk mods should be avoided
        if filters["avoid_high_risk_mods"] and option["safety_level"] == SafetyLevel.HIGH:
            return False
        
        return True
    
    def _is_compatible_with_engine(self, option: Dict[str, Any], engine_type: EngineType) -> bool:
        """Check if an option is compatible with the engine type."""
        # ECU remapping is not suitable for electric vehicles
        if "ECU" in option["name"] and engine_type == EngineType.ELECTRIC:
            return False
        
        # Some modifications may not be suitable for hybrid vehicles
        if engine_type == EngineType.HYBRID:
            # Add specific hybrid compatibility checks here
            pass
        
        return True
    
    def _adjust_priority_score(
        self, 
        recommendation: TuningRecommendation, 
        goal: DrivingGoal, 
        preferences: UserPreferences
    ) -> float:
        """Adjust priority score based on goals and preferences."""
        base_score = recommendation.priority_score
        
        # Boost score for primary goals
        if goal in preferences.primary_goals:
            base_score *= 1.2
        
        # Reduce score for high-risk modifications for beginners
        if preferences.experience_level == ExperienceLevel.BEGINNER and recommendation.safety_level == SafetyLevel.HIGH:
            base_score *= 0.7
        
        # Boost score for budget-friendly options
        if preferences.budget_range == BudgetRange.BUDGET and recommendation.cost_range["max"] < 1000:
            base_score *= 1.1
        
        return min(base_score, 10.0)
    
    def _deduplicate_recommendations(self, recommendations: List[TuningRecommendation]) -> List[TuningRecommendation]:
        """Remove duplicate recommendations based on name and category."""
        seen = set()
        unique_recommendations = []
        
        for rec in recommendations:
            key = (rec.category, rec.name)
            if key not in seen:
                seen.add(key)
                unique_recommendations.append(rec)
        
        return unique_recommendations
    
    def _filter_by_budget(self, recommendations: List[TuningRecommendation], max_budget: float) -> List[TuningRecommendation]:
        """Filter recommendations by budget and limit total recommendations."""
        filtered = []
        total_cost = 0
        
        for rec in recommendations:
            if total_cost + rec.cost_range["max"] <= max_budget:
                filtered.append(rec)
                total_cost += rec.cost_range["max"]
            else:
                # Check if we can fit the minimum cost
                if total_cost + rec.cost_range["min"] <= max_budget:
                    filtered.append(rec)
                    total_cost += rec.cost_range["min"]
        
        # Limit to top 10 recommendations
        return filtered[:10]
    
    def _calculate_total_cost(self, recommendations: List[TuningRecommendation]) -> Dict[str, float]:
        """Calculate total estimated cost range."""
        min_total = sum(rec.cost_range["min"] for rec in recommendations)
        max_total = sum(rec.cost_range["max"] for rec in recommendations)
        
        return {
            "min": min_total,
            "max": max_total,
            "currency": "USD"
        }
    
    def _generate_compatibility_matrix(self, recommendations: List[TuningRecommendation]) -> Dict[str, List[str]]:
        """Generate compatibility matrix for selected recommendations."""
        matrix = {}
        
        for rec in recommendations:
            category_key = rec.category.value
            compatible_mods = self.knowledge_base.get_compatible_modifications(category_key)
            matrix[rec.name] = compatible_mods
        
        return matrix
    
    def _generate_safety_summary(self, recommendations: List[TuningRecommendation]) -> Dict[str, List[str]]:
        """Generate safety summary for all recommendations."""
        high_risk = []
        medium_risk = []
        low_risk = []
        
        for rec in recommendations:
            if rec.safety_level == SafetyLevel.HIGH:
                high_risk.extend(rec.safety_warnings)
            elif rec.safety_level == SafetyLevel.MEDIUM:
                medium_risk.extend(rec.safety_warnings)
            else:
                low_risk.extend(rec.safety_warnings)
        
        return {
            "high_risk": list(set(high_risk)),
            "medium_risk": list(set(medium_risk)),
            "low_risk": list(set(low_risk))
        }
    
    def _generate_legal_summary(self, recommendations: List[TuningRecommendation]) -> Dict[str, List[str]]:
        """Generate legal summary for all recommendations."""
        warranty_impacts = []
        emissions_impacts = []
        insurance_impacts = []
        legal_considerations = []
        
        for rec in recommendations:
            if rec.warranty_impact != "No impact":
                warranty_impacts.append(f"{rec.name}: {rec.warranty_impact}")
            if rec.emissions_impact != "No impact":
                emissions_impacts.append(f"{rec.name}: {rec.emissions_impact}")
            if rec.insurance_impact != "No impact":
                insurance_impacts.append(f"{rec.name}: {rec.insurance_impact}")
            legal_considerations.extend(rec.legal_considerations)
        
        return {
            "warranty_impacts": list(set(warranty_impacts)),
            "emissions_impacts": list(set(emissions_impacts)),
            "insurance_impacts": list(set(insurance_impacts)),
            "legal_considerations": list(set(legal_considerations))
        }
    
    def _generate_disclaimer(self, car_info: CarInfo, user_preferences: UserPreferences) -> str:
        """Generate comprehensive disclaimer."""
        disclaimer = """
IMPORTANT DISCLAIMER:

This report provides general recommendations for car modifications and should not be considered as professional automotive advice. 

SAFETY WARNINGS:
- All modifications should be performed by qualified professionals
- Modifications may affect vehicle safety and handling characteristics
- Test all modifications in safe conditions before regular use
- Some modifications may void vehicle warranty
- Performance modifications may affect emissions compliance

LEGAL CONSIDERATIONS:
- Check local laws and regulations before making modifications
- Some modifications may be illegal for road use
- Notify your insurance company of any modifications
- Ensure modifications meet local safety standards

PROFESSIONAL CONSULTATION:
- Always consult with qualified automotive professionals
- Have modifications inspected by certified technicians
- Keep original parts for potential reversion
- Regular maintenance is critical for modified vehicles

The authors are not responsible for any damage, injury, or legal issues resulting from these modifications.
        """
        
        return disclaimer.strip() 