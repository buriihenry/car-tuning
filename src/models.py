"""
Data models for the Car Tuning AI Agent.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class EngineType(str, Enum):
    """Engine type enumeration."""
    PETROL = "petrol"
    DIESEL = "diesel"
    HYBRID = "hybrid"
    ELECTRIC = "electric"


class ExperienceLevel(str, Enum):
    """User experience level enumeration."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class DrivingGoal(str, Enum):
    """Primary driving goal enumeration."""
    PERFORMANCE = "performance"
    FUEL_ECONOMY = "fuel_economy"
    DAILY_COMFORT = "daily_comfort"
    TRACK_USE = "track_use"
    OFF_ROADING = "off_roading"


class BudgetRange(str, Enum):
    """Budget range enumeration."""
    BUDGET = "budget"  # $500-2000
    MODERATE = "moderate"  # $2000-8000
    PREMIUM = "premium"  # $8000-20000
    UNLIMITED = "unlimited"  # $20000+


class CarInfo(BaseModel):
    """Car information model."""
    make: str = Field(..., description="Car manufacturer (e.g., Toyota, BMW)")
    model: str = Field(..., description="Car model (e.g., Camry, 3 Series)")
    year: int = Field(..., ge=1900, le=2030, description="Manufacturing year")
    engine_type: EngineType = Field(..., description="Engine type")
    current_modifications: Optional[List[str]] = Field(
        default=[], description="List of current modifications"
    )

    @validator('year')
    def validate_year(cls, v):
        if v < 1900 or v > 2030:
            raise ValueError('Year must be between 1900 and 2030')
        return v


class UserPreferences(BaseModel):
    """User preferences and goals model."""
    primary_goals: List[DrivingGoal] = Field(..., description="Primary driving goals")
    budget_range: BudgetRange = Field(..., description="Available budget range")
    experience_level: ExperienceLevel = Field(..., description="User experience level")
    max_budget: Optional[float] = Field(None, ge=0, description="Maximum budget in USD")


class TuningCategory(str, Enum):
    """Tuning category enumeration."""
    ECU_REMAPPING = "ecu_remapping"
    EXHAUST_SYSTEM = "exhaust_system"
    SUSPENSION = "suspension"
    AIR_INTAKE = "air_intake"
    TIRES_WHEELS = "tires_wheels"
    BRAKE_SYSTEM = "brake_system"
    COSMETIC = "cosmetic"


class SafetyLevel(str, Enum):
    """Safety level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TuningRecommendation(BaseModel):
    """Individual tuning recommendation model."""
    category: TuningCategory = Field(..., description="Tuning category")
    name: str = Field(..., description="Modification name")
    description: str = Field(..., description="What the modification does")
    benefits: List[str] = Field(..., description="Benefits of this modification")
    cost_range: Dict[str, float] = Field(..., description="Cost range in USD")
    compatibility_notes: List[str] = Field(..., description="Compatibility considerations")
    prerequisites: List[str] = Field(..., description="Required prerequisites")
    safety_warnings: List[str] = Field(..., description="Safety warnings")
    legal_considerations: List[str] = Field(..., description="Legal considerations")
    warranty_impact: str = Field(..., description="Impact on warranty")
    emissions_impact: str = Field(..., description="Impact on emissions compliance")
    insurance_impact: str = Field(..., description="Impact on insurance")
    priority_score: float = Field(..., ge=0, le=10, description="Priority score (0-10)")
    safety_level: SafetyLevel = Field(..., description="Safety level")
    installation_difficulty: str = Field(..., description="Installation difficulty")
    professional_required: bool = Field(..., description="Whether professional installation is required")


class TuningReport(BaseModel):
    """Complete tuning recommendations report."""
    car_info: CarInfo = Field(..., description="Car information")
    user_preferences: UserPreferences = Field(..., description="User preferences")
    recommendations: List[TuningRecommendation] = Field(..., description="Tuning recommendations")
    total_estimated_cost: Dict[str, Any] = Field(..., description="Total estimated cost range")
    compatibility_matrix: Dict[str, List[str]] = Field(..., description="Compatibility matrix")
    safety_summary: Dict[str, List[str]] = Field(..., description="Safety summary")
    legal_summary: Dict[str, List[str]] = Field(..., description="Legal summary")
    disclaimer: str = Field(..., description="General disclaimer")
    generated_at: str = Field(..., description="Report generation timestamp")


class CarTuningRequest(BaseModel):
    """Complete request model for car tuning suggestions."""
    car_info: CarInfo = Field(..., description="Car information")
    user_preferences: UserPreferences = Field(..., description="User preferences") 