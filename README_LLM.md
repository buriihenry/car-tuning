# 🚗 Car Tuning AI Agent with Gemini 2.5 Flash

A sophisticated AI-powered car tuning recommendation system that combines rule-based logic with advanced language model capabilities using Google's Gemini 2.5 Flash.

## 🌟 Features

### 🤖 AI-Enhanced Recommendations
- **Gemini 2.5 Flash Integration**: Advanced language model for intelligent analysis
- **Enhanced Descriptions**: Detailed technical explanations of modifications
- **Smart Safety Analysis**: Comprehensive safety warnings and legal considerations
- **Installation Guidance**: Professional installation tips and maintenance advice
- **Cost Optimization**: Smart suggestions for better value within budget

### 🎯 Core Capabilities
- **Personalized Recommendations**: Based on car make, model, year, and engine type
- **Goal-Oriented**: Performance, fuel economy, daily comfort, track use, off-roading
- **Budget-Aware**: Multiple budget ranges with cost optimization
- **Experience-Based**: Recommendations tailored to beginner, intermediate, or advanced users
- **Safety-First**: Comprehensive safety warnings and legal compliance checks

### 🌐 Modern Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Validation**: Instant feedback on input data
- **Interactive Toggle**: Enable/disable AI enhancement
- **Beautiful UI**: Modern design with smooth animations
- **Sample Data**: Quick testing with pre-loaded examples

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google API key for Gemini 2.5 Flash (optional but recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd car-tuning
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google API key (optional)**
   ```bash
   export GOOGLE_API_KEY='your-api-key-here'
   ```

### Running the Application

#### Web Interface (Recommended)
```bash
python3 web_app.py
```
Then open your browser to: `http://localhost:5000`

#### Command Line Interface
```bash
# Interactive mode
python3 cli.py interactive

# Sample recommendations
python3 cli.py sample

# From JSON file
python3 cli.py from-file examples/sample_request.json

# Show available options
python3 cli.py options
```

#### API Testing
```bash
# Test basic functionality
python3 test_basic.py

# Test web API
python3 test_web_api.py

# Test LLM integration
python3 test_llm_integration.py
```

## 🏗️ Architecture

### Core Components

1. **`src/models.py`**: Pydantic data models for type safety
2. **`src/knowledge_base.py`**: Comprehensive tuning database
3. **`src/recommendation_engine.py`**: Rule-based recommendation logic
4. **`src/input_validator.py`**: Input validation and suggestions
5. **`src/llm_enhancer.py`**: Gemini 2.5 Flash integration
6. **`src/main.py`**: Main agent orchestrating all components

### LLM Enhancement Features

#### Enhanced Analysis
- **Technical Details**: In-depth explanations of modifications
- **Additional Benefits**: Extended benefits beyond basic descriptions
- **Safety Warnings**: Comprehensive safety considerations
- **Installation Tips**: Professional installation guidance
- **Maintenance Advice**: Long-term care recommendations

#### Custom Recommendations
- **AI-Generated**: Completely custom recommendations from LLM
- **Vehicle-Specific**: Tailored to exact make, model, and year
- **Goal-Oriented**: Aligned with user's specific goals
- **Budget-Conscious**: Optimized for user's budget constraints

## 📊 API Endpoints

### Web API
- `GET /api/options` - Get all available options
- `GET /api/sample` - Get sample request data
- `POST /api/recommendations` - Generate recommendations
- `POST /api/validate` - Validate input data
- `GET /api/llm-status` - Check LLM enhancement status
- `POST /api/custom-llm-recommendations` - Generate custom LLM recommendations

### Python API
```python
from src.main import CarTuningAgent
from src.models import CarInfo, UserPreferences, EngineType, DrivingGoal, BudgetRange, ExperienceLevel

# Initialize agent with LLM enhancement
agent = CarTuningAgent(use_llm_enhancement=True, api_key="your-api-key")

# Create car info
car_info = CarInfo(
    make="BMW",
    model="3 Series",
    year=2021,
    engine_type=EngineType.PETROL,
    current_modifications=["Sport exhaust"]
)

# Create user preferences
user_preferences = UserPreferences(
    primary_goals=[DrivingGoal.PERFORMANCE, DrivingGoal.TRACK_USE],
    budget_range=BudgetRange.PREMIUM,
    experience_level=ExperienceLevel.ADVANCED,
    max_budget=15000.0
)

# Generate recommendations
report = agent.generate_recommendations(car_info, user_preferences)

# Export results
json_output = agent.export_report_as_json(report)
```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google API key for Gemini 2.5 Flash

### LLM Enhancement Options
- **Enabled by default**: Set `use_llm_enhancement=True` in CarTuningAgent
- **Graceful fallback**: If LLM fails, falls back to rule-based recommendations
- **Toggle in web interface**: Enable/disable AI enhancement via UI

## 📈 Performance

### Without LLM Enhancement
- **Response Time**: < 1 second
- **Recommendations**: Rule-based with predefined options
- **Features**: Basic descriptions, safety warnings, cost estimates

### With LLM Enhancement
- **Response Time**: 2-5 seconds (depending on API response)
- **Recommendations**: Enhanced with AI-generated insights
- **Features**: 
  - Detailed technical explanations
  - Additional benefits and considerations
  - Enhanced safety warnings
  - Installation and maintenance tips
  - Overall analysis and professional advice

## 🛡️ Safety & Legal

### Built-in Safety Features
- **Safety Level Classification**: Low, Medium, High risk categories
- **Experience-Based Filtering**: Recommendations filtered by user experience
- **Legal Compliance**: Warranty, insurance, and emissions considerations
- **Professional Consultation**: Always recommends professional installation for complex mods

### Disclaimer System
- **Comprehensive Warnings**: Clear disclaimers about professional advice
- **Legal Considerations**: Impact on warranty, insurance, and compliance
- **Safety Guidelines**: Installation and maintenance safety tips

## 🧪 Testing

### Test Scripts
```bash
# Basic functionality test
python3 test_basic.py

# Web API test
python3 test_web_api.py

# LLM integration test
python3 test_llm_integration.py

# API functionality test
python3 test_api.py
```

### Sample Data
- `examples/sample_request.json`: BMW 3 Series performance setup
- `examples/electric_vehicle_request.json`: Tesla Model 3 example

## 🔮 Future Enhancements

### Planned Features
- **Machine Learning Integration**: Learn from user feedback
- **Image Analysis**: Analyze car photos for recommendations
- **Real-time Pricing**: Integration with parts suppliers
- **Community Features**: User reviews and ratings
- **Mobile App**: Native mobile application

### Technical Improvements
- **Caching**: Cache LLM responses for better performance
- **Batch Processing**: Handle multiple requests efficiently
- **Advanced Analytics**: Detailed usage analytics
- **API Rate Limiting**: Protect against abuse

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints throughout
- Add comprehensive docstrings
- Include unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini 2.5 Flash**: For advanced AI capabilities
- **Pydantic**: For robust data validation
- **Flask**: For the web framework
- **Tailwind CSS**: For the beautiful UI
- **Font Awesome**: For the icons

## 📞 Support

For questions, issues, or feature requests:
- Create an issue on GitHub
- Check the documentation
- Review the test examples

---

**⚠️ Important Disclaimer**: This system provides general recommendations and should not be considered as professional automotive advice. Always consult with qualified automotive professionals before making modifications to your vehicle. 