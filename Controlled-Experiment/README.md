# Controlled Experiment Analysis

Energy consumption analysis of different AI chat modes in a controlled experimental setting.

## 🔬 Experiment Overview

This project analyzes energy consumption patterns across three different AI chat modes to understand the trade-offs between performance and sustainability in conversational AI systems.

## 🎯 Research Questions

1. **Energy Efficiency**: How do different AI models compare in energy consumption?
2. **Performance Trade-offs**: What are the performance vs. sustainability trade-offs?
3. **Token Usage**: How do input/output token patterns affect energy consumption?
4. **User Behavior**: How do users adapt to different efficiency modes?

## 📁 Project Structure

```
Controlled-Experiment/
├── Raw-Data/                       # Original experiment data
│   ├── Data_Pseudonym.xlsx         # Main experiment data (Excel)
│   ├── Forms_Participants_Results/ # Participant forms
│   ├── All (not cleaned)/          # Backup/raw data files
│   ├── *.json                      # JSON data files
│   └── *.csv                       # CSV data files
└── Analysis-Scripts/               # Analysis code
    ├── matlab/                     # MATLAB analysis scripts
    ├── python/                     # Python analysis (to be created)
    └── output/                     # Generated results
        ├── plots/                  # Visualizations
        ├── data/                   # Processed data
        └── reports/                # Analysis reports
```

## 🧪 Experiment Design

### **Chat Modes**
1. **Energy Efficient Mode** (Mode 0)
   - **Model**: gpt-4.1-nano
   - **History Limit**: 2 turns
   - **Energy per Input Token**: 0.00007 Wh
   - **Energy per Output Token**: 0.00021 Wh
   - **Constant Overhead**: 0.025 Wh

2. **Balanced Mode** (Mode 1)
   - **Model**: gpt-4o-mini
   - **History Limit**: 5 turns
   - **Energy per Input Token**: 0.0001 Wh
   - **Energy per Output Token**: 0.0003 Wh
   - **Constant Overhead**: 0.03 Wh

3. **Performance Mode** (Mode 2)
   - **Model**: gpt-4o
   - **History Limit**: 10 turns
   - **Energy per Input Token**: 0.00017 Wh
   - **Energy per Output Token**: 0.00051 Wh
   - **Constant Overhead**: 0.03 Wh

### **Data Collection**
- **User Interactions**: Prompts, responses, timestamps
- **Energy Metrics**: Token-based energy consumption calculations
- **Usage Patterns**: Frequency, duration, conversation length
- **Participant Data**: Demographics, preferences, feedback

## 📊 Data Structure

### **Main Data Files**
- **`Data_Pseudonym.xlsx`**: Complete experiment data in Excel format
- **`Users.json`**: Participant information and settings
- **`Modes.json`**: Chat mode configurations and energy parameters
- **`Logs.json`**: System logs and user interactions
- **`Prompts.json`**: Individual prompt/response pairs
- **`Conversations.json`**: Complete conversation threads
- **`EnergyUnits.json`**: Energy consumption calculations

### **Key Variables**
- **`userId`**: Unique participant identifier
- **`chatMode`**: Energy efficient (0), Balanced (1), Performance (2)
- **`usage_numberOfInputTokens`**: Input token count
- **`usage_numberOfOutputTokens`**: Output token count
- **`usage_usageInWh`**: Energy consumption in Watt-hours
- **`usageInWhCorrected`**: Corrected energy calculations
- **`responseLength`**: Response text length
- **`sentAt`**: Timestamp of interaction

## 🔍 Analysis Methods

### **MATLAB Analysis** (`matlab/`)
- **`Experiment.m`**: Main analysis script
- **`InputOutput.m`**: Input/output token relationship analysis
- **`PromptLengths.m`**: Prompt length distribution analysis

### **Statistical Analysis**
- **Energy Consumption**: Per-mode energy usage patterns
- **Token Analysis**: Input/output token relationships and efficiency
- **Performance Metrics**: Response quality vs. energy consumption
- **User Behavior**: Adaptation patterns across different modes

### **Visualization**
- **Energy Consumption Charts**: Per-mode energy usage comparisons
- **Token Efficiency Plots**: Input/output token relationships
- **Performance Trade-offs**: Quality vs. sustainability visualizations
- **User Behavior Patterns**: Usage adaptation over time

## 🚀 Quick Start

### **MATLAB Analysis**
```matlab
% Navigate to MATLAB scripts directory
cd matlab/

% Run main analysis
run('Experiment.m')

% Run specific analyses
run('InputOutput.m')      % Token relationship analysis
run('PromptLengths.m')    % Prompt length analysis
```

### **Python Analysis** (To be implemented)
```bash
cd python/
pip install -r requirements.txt
python analyze_energy_consumption.py
```

## 📈 Key Findings

### **Energy Consumption Patterns**
- **Energy Efficient Mode**: Lowest energy consumption, limited context
- **Balanced Mode**: Moderate energy consumption, balanced performance
- **Performance Mode**: Highest energy consumption, full context retention

### **Token Efficiency**
- **Input Tokens**: Vary based on prompt complexity and history
- **Output Tokens**: Correlate with response length and model capability
- **Energy per Token**: Consistent across modes with different base rates

### **User Adaptation**
- **Mode Switching**: Users adapt behavior based on available context
- **Prompt Optimization**: Users modify prompts based on mode limitations
- **Usage Patterns**: Different interaction patterns across modes

## 🔧 Technical Implementation

### **Energy Modeling**
```matlab
% Energy calculation formula
energy = (inputTokens * alpha) + (outputTokens * beta) + zeta
```

Where:
- **`alpha`**: Energy per input token (Wh)
- **`beta`**: Energy per output token (Wh)  
- **`zeta`**: Constant overhead energy (Wh)

### **Data Processing**
- **Token Counting**: Automatic token calculation for all interactions
- **Energy Calculation**: Real-time energy consumption tracking
- **Aggregation**: Per-user, per-mode, and per-session summaries

## 📊 Output Structure

### **Generated Visualizations**
- **Energy Consumption Charts**: Per-mode energy usage comparisons
- **Token Efficiency Plots**: Input/output token relationships
- **Performance Trade-offs**: Quality vs. sustainability visualizations
- **User Behavior Patterns**: Usage adaptation over time

### **Statistical Reports**
- **Descriptive Statistics**: Mean, median, standard deviation
- **Correlation Analysis**: Token usage vs. energy consumption
- **Significance Testing**: Mode comparison statistical tests
- **Efficiency Metrics**: Energy per token, performance ratios

## 🎓 Research Applications

### **Academic Research**
- **Energy Efficiency Studies**: AI model energy consumption analysis
- **Sustainability Research**: Environmental impact of AI systems
- **User Behavior Studies**: Adaptation to efficiency constraints

### **Industry Applications**
- **Product Development**: Sustainable AI feature design
- **Cost Optimization**: Energy-aware AI deployment strategies
- **User Experience**: Efficiency mode user interface design

## 📋 Dependencies

### **MATLAB**
- Statistics and Machine Learning Toolbox
- Data Analysis Toolbox

### **Python** (To be implemented)
```
pandas>=1.5.0
matplotlib>=3.5.0
seaborn>=0.11.0
scipy>=1.9.0
numpy>=1.21.0
```

## 🔬 Methodology Notes

### **Energy Calculation**
- **Token-based modeling**: Energy consumption based on token usage
- **Model-specific parameters**: Different energy rates for different models
- **Constant overhead**: Base energy consumption per interaction

### **Experimental Controls**
- **Randomized assignment**: Users randomly assigned to modes
- **Consistent conditions**: Same tasks and prompts across modes
- **Data anonymization**: Participant data pseudonymized

## 📞 Support

For questions about the experiment methodology or analysis, please refer to the MATLAB script documentation or create an issue in the repository.

---

**Part of sustainable AI research initiative** 🌱
