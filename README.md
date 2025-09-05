# Sustainable LLM Chatbot Replication Package


This repository is organized into two folders:

```
├── User-Survey/                    # Survey-based attitude analysis
├── Controlled-Experiment/          # Energy consumption experiment
└── Documentation/                  # Shared research documentation
```

### **User-Survey**
- **Purpose**: Analyze user attitudes and preferences toward sustainable AI
- **Method**: Online survey with 77 participants, 29 questions
- **Focus**: Environmental concerns, usage patterns, sustainability preferences
- **Analysis**: Statistical analysis, visualization, NLP text analysis
- **Output**: 26+ publication-ready charts, theme analysis

### **Controlled-Experiment**
- **Purpose**: Measure actual energy consumption across different AI chat modes
- **Method**: Controlled experiment with 3 different chat modes
- **Focus**: Energy efficiency, token usage, performance trade-offs
- **Analysis**: MATLAB-based statistical analysis, energy modeling
- **Output**: Energy consumption charts, efficiency comparisons


## Quick Start

### **Survey Analysis**
```bash
cd User-Survey/Analysis-Scripts
pip install -r requirements.txt
python src/analyze.py
```

### **Experiment Analysis**
```bash
cd Controlled-Experiment/Analysis-Scripts/matlab
# Run MATLAB scripts for energy analysis
```

## Output Structure

### **User-Survey Outputs**
- **Demographics**: Age, profession, business domain distributions
- **Usage Patterns**: AI service usage, frequency, primary reasons
- **Environmental Attitudes**: Concern levels, importance ratings, agreement scales
- **Text Analysis**: 8 sustainability themes with representative quotes

### **Controlled-Experiment Outputs**
- **Energy Consumption**: Per-mode energy usage patterns
- **Token Analysis**: Input/output token relationships
- **Efficiency Metrics**: Energy per token, performance comparisons
- **Statistical Analysis**: Significance testing, correlation analysis

## Technical Details

### **Survey Analysis Stack**
- **Python**: pandas, matplotlib, scikit-learn, nltk
- **Visualization**: Publication-ready charts with consistent styling
- **NLP**: TF-IDF, YAKE, LDA, KMeans clustering
- **Configuration**: YAML-based styling and question definitions

### **Experiment Analysis Stack**
- **MATLAB**: Statistical analysis and visualization
- **Data**: JSON/CSV format with energy consumption metrics
- **Models**: GPT-4 variants with different efficiency profiles
- **Metrics**: Token-based energy modeling with constant overhead


This repository contains replication materials for our ongoing research on sustainable AI systems. When using this work, please cite appropriately and refer to the individual project documentation for detailed methodology and results.

