"""
LLM Enhancer module using Gemini 2.5 Flash for intelligent car tuning recommendations.
"""

import google.generativeai as genai
from typing import List, Dict, Any, Optional
import json
import os
from .models import CarInfo, UserPreferences, TuningRecommendation, TuningReport

class LLMEnhancer:
    """Enhances recommendations using Gemini 2.5 Flash."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the LLM enhancer."""
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # System prompt for car tuning expertise
        self.system_prompt = """You are an expert automotive engineer and car tuning specialist with deep knowledge of:
- Engine modifications and performance tuning
- Suspension and handling improvements
- Brake system upgrades
- Exhaust and intake systems
- Tire and wheel selection
- Safety considerations and legal compliance
- Cost estimation for automotive modifications
- Compatibility between different modifications

Your role is to analyze car information and user preferences to provide intelligent, accurate, and safe tuning recommendations. Always prioritize safety and legal compliance while maximizing performance and value for the user's specific goals and budget."""
    
    def enhance_recommendations(self, base_report: TuningReport) -> TuningReport:
        """Enhance base recommendations using Gemini 2.5 Flash."""
        try:
            # Prepare context for the LLM
            context = self._prepare_context(base_report)
            
            # Generate enhanced analysis
            enhanced_analysis = self._generate_enhanced_analysis(context)
            
            # Apply enhancements to the report
            enhanced_report = self._apply_enhancements(base_report, enhanced_analysis)
            
            return enhanced_report
            
        except Exception as e:
            print(f"Warning: LLM enhancement failed: {str(e)}")
            return base_report  # Return original report if enhancement fails
    
    def _prepare_context(self, report: TuningReport) -> str:
        """Prepare context information for the LLM."""
        car_info = report.car_info
        user_prefs = report.user_preferences
        recommendations = report.recommendations
        
        max_budget_str = f"${user_prefs.max_budget:,.0f}" if user_prefs.max_budget else "Not specified"
        
        context = f"""
CAR INFORMATION:
- Make: {car_info.make}
- Model: {car_info.model}
- Year: {car_info.year}
- Engine Type: {car_info.engine_type.value}
- Current Modifications: {', '.join(car_info.current_modifications) if car_info.current_modifications else 'None'}

USER PREFERENCES:
- Primary Goals: {', '.join([g.value for g in user_prefs.primary_goals])}
- Budget Range: {user_prefs.budget_range.value}
- Experience Level: {user_prefs.experience_level.value}
- Max Budget: {max_budget_str}

CURRENT RECOMMENDATIONS:
"""
        
        for i, rec in enumerate(recommendations, 1):
            context += f"""
{i}. {rec.name}
   - Category: {rec.category.value}
   - Cost: ${rec.cost_range['min']:,.0f} - ${rec.cost_range['max']:,.0f}
   - Priority Score: {rec.priority_score}/10
   - Safety Level: {rec.safety_level.value}
   - Description: {rec.description}
   - Benefits: {', '.join(rec.benefits)}
   - Safety Warnings: {', '.join(rec.safety_warnings)}
"""
        
        context += f"""
TOTAL ESTIMATED COST: ${report.total_estimated_cost['min']:,.0f} - ${report.total_estimated_cost['max']:,.0f}

Please analyze these recommendations and provide:
1. Enhanced descriptions with more technical details
2. Additional benefits and considerations
3. Improved safety warnings and legal considerations
4. Cost optimization suggestions
5. Alternative recommendations for better value
6. Installation tips and prerequisites
7. Long-term maintenance considerations
"""
        
        return context
    
    def _generate_enhanced_analysis(self, context: str) -> Dict[str, Any]:
        """Generate enhanced analysis using Gemini 2.5 Flash."""
        prompt = f"""
{self.system_prompt}

Please analyze the following car tuning recommendations and provide enhanced insights:

{context}

Provide your analysis in the following JSON format:
{{
    "enhanced_recommendations": [
        {{
            "original_index": 0,
            "enhanced_description": "Detailed technical description",
            "additional_benefits": ["Benefit 1", "Benefit 2"],
            "enhanced_safety_warnings": ["Warning 1", "Warning 2"],
            "installation_tips": ["Tip 1", "Tip 2"],
            "maintenance_considerations": ["Consideration 1", "Consideration 2"],
            "cost_optimization": "Suggestions for better value",
            "alternatives": ["Alternative 1", "Alternative 2"]
        }}
    ],
    "overall_analysis": {{
        "summary": "Overall assessment of the tuning plan",
        "risk_assessment": "Safety and legal risk analysis",
        "value_analysis": "Cost-benefit analysis",
        "compatibility_notes": "Notes about modification compatibility",
        "professional_advice": "Recommendations for professional consultation"
    }}
}}

Focus on providing practical, accurate, and safety-conscious advice.
"""
        
        response = self.model.generate_content(prompt)
        
        try:
            # Extract JSON from response
            content = response.text
            # Find JSON block in the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            json_str = content[start_idx:end_idx]
            
            return json.loads(json_str)
        except Exception as e:
            print(f"Error parsing LLM response: {str(e)}")
            return {"enhanced_recommendations": [], "overall_analysis": {}}
    
    def _apply_enhancements(self, base_report: TuningReport, enhanced_analysis: Dict[str, Any]) -> TuningReport:
        """Apply LLM enhancements to the base report."""
        enhanced_recommendations = []
        
        # Apply enhancements to each recommendation
        for i, rec in enumerate(base_report.recommendations):
            enhanced_rec = rec.model_copy(deep=True)
            
            # Find corresponding enhancement
            enhancement = None
            for enh in enhanced_analysis.get("enhanced_recommendations", []):
                if enh.get("original_index") == i:
                    enhancement = enh
                    break
            
            if enhancement:
                # Apply enhanced description
                if enhancement.get("enhanced_description"):
                    enhanced_rec.description = enhancement["enhanced_description"]
                
                # Add additional benefits
                if enhancement.get("additional_benefits"):
                    enhanced_rec.benefits.extend(enhancement["additional_benefits"])
                
                # Add enhanced safety warnings
                if enhancement.get("enhanced_safety_warnings"):
                    enhanced_rec.safety_warnings.extend(enhancement["enhanced_safety_warnings"])
                
                # Add installation tips and maintenance considerations
                installation_tips = enhancement.get("installation_tips", [])
                maintenance_considerations = enhancement.get("maintenance_considerations", [])
                
                if installation_tips or maintenance_considerations:
                    enhanced_rec.legal_considerations.extend([
                        f"Installation: {'; '.join(installation_tips)}" if installation_tips else "",
                        f"Maintenance: {'; '.join(maintenance_considerations)}" if maintenance_considerations else ""
                    ])
                    # Remove empty strings
                    enhanced_rec.legal_considerations = [item for item in enhanced_rec.legal_considerations if item]
            
            enhanced_recommendations.append(enhanced_rec)
        
        # Create enhanced report
        enhanced_report = base_report.model_copy(deep=True)
        enhanced_report.recommendations = enhanced_recommendations
        
        # Add overall analysis to the report
        overall_analysis = enhanced_analysis.get("overall_analysis", {})
        if overall_analysis:
            enhanced_report.disclaimer += f"\n\nAI-Enhanced Analysis:\n"
            if overall_analysis.get("summary"):
                enhanced_report.disclaimer += f"Summary: {overall_analysis['summary']}\n"
            if overall_analysis.get("risk_assessment"):
                enhanced_report.disclaimer += f"Risk Assessment: {overall_analysis['risk_assessment']}\n"
            if overall_analysis.get("value_analysis"):
                enhanced_report.disclaimer += f"Value Analysis: {overall_analysis['value_analysis']}\n"
            if overall_analysis.get("professional_advice"):
                enhanced_report.disclaimer += f"Professional Advice: {overall_analysis['professional_advice']}\n"
        
        return enhanced_report
    
    def generate_custom_recommendations(self, car_info: CarInfo, user_preferences: UserPreferences) -> List[Dict[str, Any]]:
        """Generate custom recommendations using Gemini 2.5 Flash."""
        max_budget_str = f"${user_preferences.max_budget:,.0f}" if user_preferences.max_budget else "Not specified"
        
        prompt = f"""
{self.system_prompt}

Generate custom car tuning recommendations for the following vehicle and preferences:

CAR INFORMATION:
- Make: {car_info.make}
- Model: {car_info.model}
- Year: {car_info.year}
- Engine Type: {car_info.engine_type.value}
- Current Modifications: {', '.join(car_info.current_modifications) if car_info.current_modifications else 'None'}

USER PREFERENCES:
- Primary Goals: {', '.join([g.value for g in user_preferences.primary_goals])}
- Budget Range: {user_preferences.budget_range.value}
- Experience Level: {user_preferences.experience_level.value}
- Max Budget: {max_budget_str}

Please provide 5-8 custom tuning recommendations in the following JSON format:
{{
    "recommendations": [
        {{
            "name": "Recommendation Name",
            "category": "ecu_tuning|exhaust_system|air_intake|suspension|tires_wheels|brake_system|cosmetic",
            "description": "Detailed description of the modification",
            "cost_range": {{"min": 1000, "max": 3000}},
            "priority_score": 8.5,
            "safety_level": "low|medium|high",
            "installation_difficulty": "Easy|Moderate|Advanced",
            "benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
            "safety_warnings": ["Warning 1", "Warning 2"],
            "legal_considerations": ["Legal consideration 1", "Legal consideration 2"],
            "compatibility_notes": "Notes about compatibility with other modifications",
            "professional_installation_required": true/false
        }}
    ]
}}

Focus on:
1. Safety and legal compliance
2. Value for money within the budget
3. Suitability for the user's experience level
4. Compatibility with the specific vehicle
5. Alignment with the user's goals
"""
        
        response = self.model.generate_content(prompt)
        
        try:
            content = response.text
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            json_str = content[start_idx:end_idx]
            
            result = json.loads(json_str)
            return result.get("recommendations", [])
        except Exception as e:
            print(f"Error generating custom recommendations: {str(e)}")
            return [] 