# Sustainable LLM Chatbot Replication Package

This repository contains a comprehensive research package for studying sustainable AI chatbot usage patterns and user preferences. It includes two complementary projects that analyze different aspects of sustainable LLM deployment.

## 📁 Repository Structure

```
Sustainable-LLM-chatbot-replication-package/
├── survey analyzer/          # Python-based survey data analysis
├── user experiment/          # MATLAB-based experimental data analysis
└── README.md                # This file
```

## 🔬 Overview

This package supports research on **sustainable AI chatbot deployment** by providing tools to:

1. **Analyze user attitudes** toward energy-efficient AI services
2. **Measure actual energy consumption** across different chatbot modes
3. **Study usage patterns** and behavioral changes over time
4. **Evaluate the trade-offs** between performance and energy efficiency

## 📊 Projects

### 1. Survey Analyzer (`survey analyzer/`)
- **Purpose**: Analyze user survey data about LLM chatbot preferences and environmental concerns
- **Technology**: Python (pandas, matplotlib)
- **Focus**: Demographics, environmental attitudes, usage preferences
- **Output**: Comprehensive visualizations of survey responses

### 2. User Experiment (`user experiment/`)
- **Purpose**: Analyze experimental data from users interacting with different chatbot modes
- **Technology**: MATLAB
- **Focus**: Energy consumption, usage patterns, behavioral analysis
- **Output**: Statistical analysis and energy efficiency comparisons

## 🚀 Quick Start

### Survey Analyzer
```bash
cd "survey analyzer"
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/analyze.py
```

### User Experiment
```bash
cd "user experiment"
# Open MATLAB and run Experiment.m
```


## 🔧 Requirements

- **Survey Analyzer**: Python 3.7+, pandas, matplotlib, openpyxl
- **User Experiment**: MATLAB R2019b or later

## 📝 Data Description

- **Survey Data**: User responses about AI usage preferences and environmental concerns
- **Experimental Data**: Real user interactions with different chatbot modes, including:
  - Conversation logs and prompts
  - Energy consumption measurements
  - User behavior metrics
  - Daily usage patterns

## 📚 Usage

Each project can be run independently:

1. **For survey analysis**: Use the Survey Analyzer to process and visualize survey responses
2. **For experimental analysis**: Use the User Experiment tools to analyze behavioral and energy consumption data

## 🤝 Contributing

This is a research replication package. Please refer to the individual project READMEs for specific setup and usage instructions.

## 📄 License

Please refer to the original research paper for licensing and citation information.
