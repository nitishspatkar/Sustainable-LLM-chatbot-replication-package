# Controlled Experiment Analysis

Energy consumption analysis of different AI chat modes in a controlled experimental setting. This project analyzes energy consumption patterns across three different AI chat modes to understand the trade-offs between performance and sustainability in conversational AI systems.

## Folder Structure

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
    ├── python/                     # Python analysis scripts
    └── output/                     # Generated results
        ├── plots/                  # Visualizations
        ├── data/                   # Processed data
        └── reports/                # Analysis reports
```

## Quick Start

### **MATLAB Analysis**
```matlab
cd matlab/
run('Experiment.m')        # Main analysis
run('InputOutput.m')       # Token relationship analysis
run('PromptLengths.m')     # Prompt length analysis
```

### **Python Analysis**
```bash
cd python/
pip install -r requirements.txt
python run_all_analyses.py  # Run all Python analyses
```

## Chat Modes

1. **Energy Efficient Mode** (Mode 0)
   - Model: gpt-4.1-nano, History: 2 turns
   - Energy: 0.00007 Wh/input token, 0.00021 Wh/output token

2. **Balanced Mode** (Mode 1)
   - Model: gpt-4o-mini, History: 5 turns
   - Energy: 0.0001 Wh/input token, 0.0003 Wh/output token

3. **Performance Mode** (Mode 2)
   - Model: gpt-4o, History: 10 turns
   - Energy: 0.00017 Wh/input token, 0.00051 Wh/output token

## Dependencies

### **MATLAB**
- Statistics and Machine Learning Toolbox
- Data Analysis Toolbox

### **Python**
```
pandas>=1.5.0
matplotlib>=3.5.0
seaborn>=0.11.0
scipy>=1.9.0
numpy>=1.21.0
```
