# Car Tuning AI Agent

A vibe-coded comprehensive AI agent that provides personalized car tuning suggestions based on user input, considering performance goals, budget, experience level, and safety requirements.

## 🚗 Features

### Core Functionality
- **Personalized Recommendations**: Generate tuning suggestions based on your specific vehicle and goals
- **Safety-First Approach**: Comprehensive safety warnings and legal considerations
- **Budget-Aware**: Recommendations filtered by your available budget
- **Experience-Based**: Suggestions tailored to your mechanical experience level
- **Compatibility Checking**: Ensures modifications work together properly

### Supported Modifications
- **ECU Remapping/Chip Tuning**: Engine performance optimization
- **Exhaust System Upgrades**: Improved flow and sound
- **Suspension & Handling**: Coilovers, lowering springs, alignment
- **Air Intake Systems**: Cold air intakes, performance filters
- **Tires & Wheels**: Performance tires, lightweight wheels
- **Brake System Upgrades**: Performance pads, big brake kits
- **Cosmetic Modifications**: Body kits, aesthetic improvements

### Vehicle Support
- **Engine Types**: Petrol, Diesel, Hybrid, Electric
- **Car Makes**: Toyota, BMW, Mercedes-Benz, Tesla, Porsche, and many more
- **Year Range**: 1900-2030
- **Experience Levels**: Beginner, Intermediate, Advanced

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd car-tuning

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Command Line Interface

#### Interactive Mode
Start an interactive session to input your vehicle and preferences:
```bash
python cli.py interactive
```

#### Sample Report
Generate a sample recommendation report:
```bash
python cli.py sample
```

#### From JSON File
Generate recommendations from a JSON file:
```bash
python cli.py from-file examples/sample_request.json
```

#### View Available Options
See all supported options:
```bash
python cli.py options
```

### Python API

#### Basic Usage
```python
from src.main import CarTuningAgent
from src.models import CarInfo, UserPreferences, EngineType, DrivingGoal, BudgetRange, ExperienceLevel

# Create agent
agent = CarTuningAgent()

# Define car information
car_info = CarInfo(
    make="BMW",
    model="3 Series",
    year=2021,
    engine_type=EngineType.PETROL,
    current_modifications=[]
)

# Define user preferences
user_preferences = UserPreferences(
    primary_goals=[DrivingGoal.PERFORMANCE, DrivingGoal.TRACK_USE],
    budget_range=BudgetRange.PREMIUM,
    experience_level=ExperienceLevel.ADVANCED,
    max_budget=15000.0
)

# Generate recommendations
report = agent.generate_recommendations(car_info, user_preferences)

# Export to JSON
json_report = agent.export_report_as_json(report)
print(json_report)
```

#### From JSON Data
```python
import json

# Load request data
with open('request.json', 'r') as f:
    request_data = json.load(f)

# Generate recommendations
agent = CarTuningAgent()
report = agent.generate_recommendations_from_dict(request_data)
```

## 📋 Input Format

### Car Information
```json
{
  "car_info": {
    "make": "BMW",
    "model": "3 Series",
    "year": 2021,
    "engine_type": "petrol",
    "current_modifications": [
      "Performance air filter",
      "Lowering springs"
    ]
  }
}
```

### User Preferences
```json
{
  "user_preferences": {
    "primary_goals": ["performance", "track_use"],
    "budget_range": "premium",
    "experience_level": "advanced",
    "max_budget": 15000.0
  }
}
```

### Available Options

#### Engine Types
- `petrol` - Gasoline engines
- `diesel` - Diesel engines
- `hybrid` - Hybrid vehicles
- `electric` - Electric vehicles

#### Driving Goals
- `performance` - Power and speed improvements
- `fuel_economy` - Better fuel efficiency
- `daily_comfort` - Comfort and usability
- `track_use` - Track/racing modifications
- `off_roading` - Off-road capabilities

#### Budget Ranges
- `budget` - $500-$2,000
- `moderate` - $2,000-$8,000
- `premium` - $8,000-$20,000
- `unlimited` - $20,000+

#### Experience Levels
- `beginner` - Limited mechanical experience
- `intermediate` - Some modification experience
- `advanced` - Extensive modification experience

## 📊 Output Format

The system generates comprehensive reports including:

### Recommendations
- **Modification Details**: Name, description, benefits
- **Cost Estimates**: Minimum and maximum cost ranges
- **Safety Information**: Warnings and risk levels
- **Legal Considerations**: Warranty, emissions, insurance impacts
- **Installation Requirements**: Difficulty and professional requirements
- **Priority Scores**: 0-10 ranking based on goals and budget

### Safety & Legal Summary
- **High Risk Warnings**: Critical safety considerations
- **Warranty Impacts**: How modifications affect vehicle warranty
- **Emissions Compliance**: Impact on emissions testing
- **Insurance Considerations**: Effects on insurance coverage

### Compatibility Matrix
- **Modification Compatibility**: Which modifications work together
- **Prerequisites**: Required modifications before others
- **Conflicts**: Incompatible modification combinations

## 🔒 Safety & Legal Considerations

### Important Disclaimers
- All recommendations are for informational purposes only
- Professional installation is recommended for most modifications
- Some modifications may void vehicle warranty
- Check local laws and regulations before modifications
- Notify insurance company of any modifications
- Test modifications in safe conditions before regular use

### Safety Guidelines
- **Beginner Level**: Focus on low-risk, professional-installation modifications
- **Intermediate Level**: Moderate-risk modifications with proper guidance
- **Advanced Level**: High-performance modifications with full understanding of risks

## 🏗️ Architecture

### Modular Design
```
src/
├── models.py              # Data models and enums
├── knowledge_base.py      # Tuning options and compatibility data
├── recommendation_engine.py # Core recommendation logic
├── input_validator.py     # Input validation and error handling
└── main.py               # Main application interface
```

### Key Components
- **Knowledge Base**: Comprehensive database of tuning options
- **Recommendation Engine**: Rules-based recommendation system
- **Input Validator**: Data validation and error handling
- **CLI Interface**: User-friendly command-line interface

## 🧪 Testing

### Run Sample Tests
```bash
# Test with sample data
python cli.py sample

# Test with different vehicle types
python cli.py from-file examples/electric_vehicle_request.json
```

### Validation Examples
```python
from src.main import CarTuningAgent

agent = CarTuningAgent()

# Validate car information
car_info = CarInfo(...)
is_valid, errors = agent.validate_car_info(car_info)

# Get suggestions
suggestions = agent.get_car_make_suggestions("Toy")
```

## 🔧 Development

### Adding New Modifications
1. Update `knowledge_base.py` with new tuning options
2. Add compatibility information
3. Update safety guidelines
4. Test with different vehicle types

### Extending Vehicle Support
1. Add new makes/models to `input_validator.py`
2. Update engine compatibility matrix
3. Test validation and recommendations

### Customizing Recommendations
1. Modify priority scoring in `recommendation_engine.py`
2. Adjust experience-based filters
3. Update budget range calculations

## 📈 Future Enhancements

### Planned Features
- **Machine Learning Integration**: ML-based recommendation improvements
- **Real-time Pricing**: Live cost estimates from suppliers
- **Installation Guides**: Step-by-step modification instructions
- **Community Reviews**: User feedback and ratings
- **Mobile App**: iOS/Android application
- **Web Interface**: Browser-based recommendation tool

### API Integration
- **External Databases**: Real-time vehicle data
- **Parts Suppliers**: Live inventory and pricing
- **Professional Networks**: Connect with certified installers

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints throughout
- Add comprehensive docstrings
- Include unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This software provides general recommendations for car modifications and should not be considered as professional automotive advice. Always consult with qualified automotive professionals before making any modifications to your vehicle. The authors are not responsible for any damage, injury, or legal issues resulting from these modifications.

## 📞 Support

For questions, issues, or feature requests:
- Create an issue on GitHub
- Check the documentation
- Review the examples directory

---

**Built with ❤️ for car enthusiasts who want to make informed modification decisions.** # car-tuning
