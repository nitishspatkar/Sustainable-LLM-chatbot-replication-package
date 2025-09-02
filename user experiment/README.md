# User Experiment Analysis

A MATLAB-based analysis toolkit for studying user behavior and energy consumption patterns in sustainable AI chatbot experiments.

## 📋 Overview

This project analyzes experimental data from users interacting with different chatbot modes to understand the relationship between AI performance, energy consumption, and user behavior.

## 🎯 Research Focus

- **Energy Consumption Analysis**: Compare energy usage across different chatbot modes
- **User Behavior Patterns**: Analyze how users adapt their usage based on energy awareness
- **Performance vs. Efficiency Trade-offs**: Evaluate the balance between response quality and energy consumption
- **Temporal Usage Patterns**: Study how usage patterns change over time

## 📁 Project Structure

```
user experiment/
├── Data.xlsx                    # Main experimental dataset
├── Data_Pseudonym.xlsx          # Pseudonymized version
├── Experiment.m                 # Main analysis script
├── InputOutput.m               # Input/output analysis
├── PromptLengths.m             # Prompt length analysis
├── Forms_Participants_Results/ # Survey responses
│   ├── DailyCheckIn.xlsx
│   └── FinalQuestionnaire.xlsx
├── All (not cleaned)/          # Raw experimental data
└── *.csv, *.json               # Processed data files
```

## 🔬 Experimental Design

The experiment compares three chatbot modes:
- **Energy Efficient**: Optimized for minimal energy consumption
- **Balanced**: Moderate energy usage with good performance
- **Performance**: Maximum performance with higher energy consumption

## 📊 Data Components

### Core Datasets
- **Users**: Participant information and demographics
- **Prompts**: User queries and chatbot responses
- **Conversations**: Complete conversation threads
- **Logs**: System logs and user interactions
- **EnergyUnits**: Energy consumption measurements

### Analysis Scripts
- **Experiment.m**: Main statistical analysis and visualization
- **InputOutput.m**: Input/output token and energy analysis
- **PromptLengths.m**: Prompt length distribution analysis

## 🚀 Usage

### Prerequisites
- MATLAB R2019b or later
- Statistics and Machine Learning Toolbox (recommended)

### Running the Analysis

1. **Main Analysis**:
   ```matlab
   % Open MATLAB and navigate to the user experiment directory
   run('Experiment.m')
   ```

2. **Input/Output Analysis**:
   ```matlab
   run('InputOutput.m')
   ```

3. **Prompt Length Analysis**:
   ```matlab
   run('PromptLengths.m')
   ```

## 📈 Key Metrics

### Energy Consumption
- Total energy usage per mode (Wh)
- Energy per prompt
- Energy per token (input/output)

### Usage Patterns
- Prompts per user per day
- Mode preference distribution
- Daily usage trends
- Session duration and frequency

### Performance Metrics
- Response length and quality
- User satisfaction indicators
- Completion rates

## 📊 Output Visualizations

The analysis generates several key visualizations:

- **Energy Usage Comparison**: Bar charts comparing energy consumption across modes
- **Usage Patterns**: Line charts showing daily usage trends
- **Mode Preferences**: Stacked bar charts of mode usage over time
- **Prompt Analysis**: Distribution of prompt lengths and types

## 🔍 Key Findings

The analysis reveals:
- Significant energy consumption differences between modes
- User adaptation patterns when energy information is provided
- Trade-offs between performance and efficiency preferences
- Temporal patterns in sustainable AI usage

## 📝 Data Privacy

- **Data_Pseudonym.xlsx**: Contains pseudonymized data for analysis
- **All (not cleaned)/**: Contains raw data with original identifiers
- All personal information has been anonymized for research purposes

## 🛠️ Customization

### Adding New Metrics
1. Modify the data loading section in `Experiment.m`
2. Add new calculation columns to the analysis tables
3. Create corresponding visualization code

### Extending Analysis
- Add new time-based analyses by modifying the grouping functions
- Include additional user demographic factors
- Implement new energy efficiency metrics

## 📚 Dependencies

- MATLAB Base
- Statistics and Machine Learning Toolbox (for advanced statistical functions)
- No external toolboxes required for basic functionality

## 🔧 Troubleshooting

### Common Issues
1. **Memory Issues**: For large datasets, consider processing in chunks
2. **Missing Data**: The scripts handle missing values with appropriate defaults
3. **Date Format**: Ensure date columns are properly formatted as datetime objects

### Performance Tips
- Use the pseudonymized dataset for faster processing
- Close unnecessary figures to free memory
- Consider parallel processing for large-scale analyses

## 📄 Citation

Please cite the original research paper when using this analysis package.
