"""
Knowledge base for car tuning recommendations.
Contains tuning options, compatibility data, and safety information.
"""

from typing import Dict, List, Any
from .models import (
    TuningCategory, EngineType, DrivingGoal, BudgetRange, 
    ExperienceLevel, SafetyLevel, TuningRecommendation
)


class TuningKnowledgeBase:
    """Knowledge base containing all tuning options and compatibility data."""
    
    def __init__(self):
        self.tuning_options = self._initialize_tuning_options()
        self.compatibility_matrix = self._initialize_compatibility_matrix()
        self.budget_ranges = self._get_budget_ranges()
        self.safety_guidelines = self._get_safety_guidelines()
    
    def _initialize_tuning_options(self) -> Dict[TuningCategory, List[Dict[str, Any]]]:
        """Initialize all available tuning options."""
        return {
            TuningCategory.ECU_REMAPPING: [
                {
                    "name": "Stage 1 ECU Remap",
                    "description": "Optimizes fuel injection, ignition timing, and boost pressure for improved performance",
                    "benefits": ["10-20% power increase", "Better throttle response", "Improved fuel efficiency"],
                    "cost_range": {"min": 300, "max": 800},
                    "compatibility_notes": ["Compatible with most modern petrol and diesel engines", "Requires OBD-II port"],
                    "prerequisites": ["Stock engine in good condition", "No existing ECU modifications"],
                    "safety_warnings": ["May void warranty", "Ensure professional installation"],
                    "legal_considerations": ["Check local emissions laws", "May affect insurance"],
                    "warranty_impact": "Likely to void powertrain warranty",
                    "emissions_impact": "May affect emissions compliance",
                    "insurance_impact": "May require insurance notification",
                    "priority_score": 9.0,
                    "safety_level": SafetyLevel.MEDIUM,
                    "installation_difficulty": "Professional installation required",
                    "professional_required": True
                },
                {
                    "name": "Stage 2 ECU Remap",
                    "description": "Advanced ECU tuning for modified engines with supporting hardware",
                    "benefits": ["20-35% power increase", "Enhanced torque delivery", "Customizable power curves"],
                    "cost_range": {"min": 500, "max": 1200},
                    "compatibility_notes": ["Requires supporting modifications", "Not suitable for stock engines"],
                    "prerequisites": ["Stage 1 remap", "Upgraded air intake", "Performance exhaust"],
                    "safety_warnings": ["High risk of engine damage if not properly tuned", "Requires supporting hardware"],
                    "legal_considerations": ["Likely illegal for road use", "Track use only"],
                    "warranty_impact": "Will void warranty",
                    "emissions_impact": "Will fail emissions testing",
                    "insurance_impact": "Will affect insurance coverage",
                    "priority_score": 8.5,
                    "safety_level": SafetyLevel.HIGH,
                    "installation_difficulty": "Professional installation required",
                    "professional_required": True
                }
            ],
            
            TuningCategory.EXHAUST_SYSTEM: [
                {
                    "name": "Performance Exhaust System",
                    "description": "Replaces stock exhaust with high-flow system for better performance and sound",
                    "benefits": ["5-15% power increase", "Improved exhaust flow", "Enhanced engine sound"],
                    "cost_range": {"min": 400, "max": 2000},
                    "compatibility_notes": ["Compatible with most vehicles", "Check local noise regulations"],
                    "prerequisites": ["Stock exhaust system"],
                    "safety_warnings": ["Ensure proper fitment", "Check for leaks after installation"],
                    "legal_considerations": ["Check local noise regulations", "May require emissions testing"],
                    "warranty_impact": "May affect exhaust warranty",
                    "emissions_impact": "May affect emissions compliance",
                    "insurance_impact": "Minimal impact",
                    "priority_score": 7.5,
                    "safety_level": SafetyLevel.LOW,
                    "installation_difficulty": "Moderate - professional recommended",
                    "professional_required": False
                },
                {
                    "name": "Cat-Back Exhaust System",
                    "description": "Replaces exhaust from catalytic converter back for improved flow",
                    "benefits": ["3-8% power increase", "Better exhaust flow", "Sportier sound"],
                    "cost_range": {"min": 300, "max": 1500},
                    "compatibility_notes": ["Maintains catalytic converter", "Generally street legal"],
                    "prerequisites": ["Stock exhaust system"],
                    "safety_warnings": ["Ensure proper fitment", "Check for leaks"],
                    "legal_considerations": ["Generally street legal", "Check local regulations"],
                    "warranty_impact": "Minimal impact",
                    "emissions_impact": "Minimal impact",
                    "insurance_impact": "Minimal impact",
                    "priority_score": 7.0,
                    "safety_level": SafetyLevel.LOW,
                    "installation_difficulty": "Moderate",
                    "professional_required": False
                }
            ],
            
            TuningCategory.AIR_INTAKE: [
                {
                    "name": "Cold Air Intake System",
                    "description": "Replaces stock air filter with high-flow system for better air delivery",
                    "benefits": ["3-8% power increase", "Improved throttle response", "Better engine breathing"],
                    "cost_range": {"min": 150, "max": 500},
                    "compatibility_notes": ["Compatible with most vehicles", "Check engine bay space"],
                    "prerequisites": ["Stock air intake system"],
                    "safety_warnings": ["Ensure proper fitment", "Check for air leaks"],
                    "legal_considerations": ["Generally street legal", "May require CARB approval"],
                    "warranty_impact": "Minimal impact",
                    "emissions_impact": "Minimal impact",
                    "insurance_impact": "Minimal impact",
                    "priority_score": 6.5,
                    "safety_level": SafetyLevel.LOW,
                    "installation_difficulty": "Easy to moderate",
                    "professional_required": False
                },
                {
                    "name": "Performance Air Filter",
                    "description": "High-flow air filter for improved air flow",
                    "benefits": ["1-3% power increase", "Better air flow", "Reusable"],
                    "cost_range": {"min": 50, "max": 200},
                    "compatibility_notes": ["Compatible with most vehicles", "Check filter size"],
                    "prerequisites": ["Stock air filter"],
                    "safety_warnings": ["Ensure proper fitment", "Regular cleaning required"],
                    "legal_considerations": ["Generally street legal"],
                    "warranty_impact": "Minimal impact",
                    "emissions_impact": "No impact",
                    "insurance_impact": "No impact",
                    "priority_score": 5.0,
                    "safety_level": SafetyLevel.LOW,
                    "installation_difficulty": "Easy",
                    "professional_required": False
                }
            ],
            
            TuningCategory.SUSPENSION: [
                {
                    "name": "Lowering Springs",
                    "description": "Lower ride height and improve handling with stiffer springs",
                    "benefits": ["Improved handling", "Lower center of gravity", "Sportier appearance"],
                    "cost_range": {"min": 200, "max": 800},
                    "compatibility_notes": ["Check spring rates for your vehicle", "May require shock upgrades"],
                    "prerequisites": ["Stock suspension"],
                    "safety_warnings": ["May affect ride quality", "Check ground clearance"],
                    "legal_considerations": ["Check local height restrictions", "May affect safety inspections"],
                    "warranty_impact": "May affect suspension warranty",
                    "emissions_impact": "No impact",
                    "insurance_impact": "Minimal impact",
                    "priority_score": 6.0,
                    "safety_level": SafetyLevel.MEDIUM,
                    "installation_difficulty": "Moderate - professional recommended",
                    "professional_required": False
                },
                {
                    "name": "Coilover Suspension",
                    "description": "Adjustable suspension system for maximum handling and ride height control",
                    "benefits": ["Fully adjustable ride height", "Improved handling", "Customizable damping"],
                    "cost_range": {"min": 800, "max": 3000},
                    "compatibility_notes": ["Check vehicle compatibility", "Professional setup recommended"],
                    "prerequisites": ["Stock suspension"],
                    "safety_warnings": ["Professional installation required", "Proper setup critical"],
                    "legal_considerations": ["Check local height restrictions", "May require certification"],
                    "warranty_impact": "Will affect suspension warranty",
                    "emissions_impact": "No impact",
                    "insurance_impact": "May affect insurance",
                    "priority_score": 7.5,
                    "safety_level": SafetyLevel.MEDIUM,
                    "installation_difficulty": "Professional installation required",
                    "professional_required": True
                }
            ],
            
            TuningCategory.TIRES_WHEELS: [
                {
                    "name": "Performance Tires",
                    "description": "High-performance tires for improved grip and handling",
                    "benefits": ["Better grip", "Improved handling", "Shorter braking distances"],
                    "cost_range": {"min": 400, "max": 1200},
                    "compatibility_notes": ["Check tire size compatibility", "Consider wheel size"],
                    "prerequisites": ["Compatible wheels"],
                    "safety_warnings": ["Shorter tread life", "May affect ride quality"],
                    "legal_considerations": ["Must meet DOT standards", "Check local regulations"],
                    "warranty_impact": "No impact",
                    "emissions_impact": "No impact",
                    "insurance_impact": "No impact",
                    "priority_score": 8.0,
                    "safety_level": SafetyLevel.LOW,
                    "installation_difficulty": "Professional installation recommended",
                    "professional_required": False
                },
                {
                    "name": "Lightweight Wheels",
                    "description": "Lightweight alloy wheels for reduced unsprung weight",
                    "benefits": ["Reduced unsprung weight", "Improved handling", "Better acceleration"],
                    "cost_range": {"min": 600, "max": 2000},
                    "compatibility_notes": ["Check bolt pattern and offset", "Consider tire compatibility"],
                    "prerequisites": ["Compatible bolt pattern"],
                    "safety_warnings": ["Ensure proper fitment", "Check load rating"],
                    "legal_considerations": ["Must meet safety standards", "Check local regulations"],
                    "warranty_impact": "No impact",
                    "emissions_impact": "No impact",
                    "insurance_impact": "No impact",
                    "priority_score": 6.5,
                    "safety_level": SafetyLevel.LOW,
                    "installation_difficulty": "Professional installation recommended",
                    "professional_required": False
                }
            ],
            
            TuningCategory.BRAKE_SYSTEM: [
                {
                    "name": "Performance Brake Pads",
                    "description": "High-performance brake pads for improved stopping power",
                    "benefits": ["Better stopping power", "Improved fade resistance", "Better pedal feel"],
                    "cost_range": {"min": 100, "max": 400},
                    "compatibility_notes": ["Check pad compatibility", "May require rotor upgrade"],
                    "prerequisites": ["Stock brake system"],
                    "safety_warnings": ["May produce more dust", "Bed-in procedure required"],
                    "legal_considerations": ["Must meet safety standards"],
                    "warranty_impact": "May affect brake warranty",
                    "emissions_impact": "No impact",
                    "insurance_impact": "No impact",
                    "priority_score": 7.0,
                    "safety_level": SafetyLevel.MEDIUM,
                    "installation_difficulty": "Moderate - professional recommended",
                    "professional_required": False
                },
                {
                    "name": "Big Brake Kit",
                    "description": "Larger brake rotors and calipers for maximum stopping power",
                    "benefits": ["Maximum stopping power", "Better heat dissipation", "Improved fade resistance"],
                    "cost_range": {"min": 1500, "max": 5000},
                    "compatibility_notes": ["Check wheel clearance", "May require wheel upgrade"],
                    "prerequisites": ["Compatible wheels", "Sufficient wheel clearance"],
                    "safety_warnings": ["Professional installation required", "Proper bleeding critical"],
                    "legal_considerations": ["Must meet safety standards", "May require certification"],
                    "warranty_impact": "Will affect brake warranty",
                    "emissions_impact": "No impact",
                    "insurance_impact": "May affect insurance",
                    "priority_score": 8.5,
                    "safety_level": SafetyLevel.HIGH,
                    "installation_difficulty": "Professional installation required",
                    "professional_required": True
                }
            ],
            
            TuningCategory.COSMETIC: [
                {
                    "name": "Body Kit",
                    "description": "Aesthetic modifications for improved appearance",
                    "benefits": ["Improved appearance", "Better aerodynamics", "Personalization"],
                    "cost_range": {"min": 500, "max": 3000},
                    "compatibility_notes": ["Check fitment", "May require paint matching"],
                    "prerequisites": ["Stock body panels"],
                    "safety_warnings": ["Ensure proper fitment", "Check for sharp edges"],
                    "legal_considerations": ["Check local regulations", "May require certification"],
                    "warranty_impact": "No impact on mechanical warranty",
                    "emissions_impact": "No impact",
                    "insurance_impact": "May affect insurance",
                    "priority_score": 3.0,
                    "safety_level": SafetyLevel.LOW,
                    "installation_difficulty": "Moderate - professional recommended",
                    "professional_required": False
                }
            ]
        }
    
    def _initialize_compatibility_matrix(self) -> Dict[str, List[str]]:
        """Initialize compatibility matrix for tuning modifications."""
        return {
            "ecu_remapping": ["air_intake", "exhaust_system"],
            "exhaust_system": ["ecu_remapping", "air_intake"],
            "air_intake": ["ecu_remapping", "exhaust_system"],
            "suspension": ["tires_wheels", "brake_system"],
            "tires_wheels": ["suspension", "brake_system"],
            "brake_system": ["suspension", "tires_wheels"],
            "cosmetic": []  # Cosmetic mods are generally compatible with everything
        }
    
    def _get_budget_ranges(self) -> Dict[BudgetRange, Dict[str, float]]:
        """Get budget range definitions."""
        return {
            BudgetRange.BUDGET: {"min": 500, "max": 2000},
            BudgetRange.MODERATE: {"min": 2000, "max": 8000},
            BudgetRange.PREMIUM: {"min": 8000, "max": 20000},
            BudgetRange.UNLIMITED: {"min": 20000, "max": 100000}
        }
    
    def _get_safety_guidelines(self) -> Dict[str, List[str]]:
        """Get safety guidelines for different modification types."""
        return {
            "general": [
                "Always consult with professionals for major modifications",
                "Ensure all modifications meet local safety standards",
                "Test modifications in safe conditions before regular use",
                "Keep original parts for potential reversion"
            ],
            "performance": [
                "Ensure supporting modifications are in place",
                "Monitor engine parameters after ECU modifications",
                "Use appropriate fuel and oil for modified engines",
                "Regular maintenance is critical for modified vehicles"
            ],
            "suspension": [
                "Professional alignment required after suspension modifications",
                "Check ground clearance after lowering",
                "Ensure proper shock/spring matching",
                "Test handling characteristics before aggressive driving"
            ],
            "brakes": [
                "Professional installation recommended for brake modifications",
                "Proper bleeding of brake system is critical",
                "Bed-in new brake pads properly",
                "Test brake performance before regular use"
            ]
        }
    
    def get_tuning_options_for_category(self, category: TuningCategory) -> List[Dict[str, Any]]:
        """Get all tuning options for a specific category."""
        return self.tuning_options.get(category, [])
    
    def get_compatible_modifications(self, modification: str) -> List[str]:
        """Get list of modifications compatible with the given modification."""
        return self.compatibility_matrix.get(modification, [])
    
    def get_budget_range(self, budget_range: BudgetRange) -> Dict[str, float]:
        """Get budget range for the given budget level."""
        return self.budget_ranges.get(budget_range, {"min": 0, "max": 0})
    
    def get_safety_guidelines(self, category: str = "general") -> List[str]:
        """Get safety guidelines for the given category."""
        return self.safety_guidelines.get(category, []) 