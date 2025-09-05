# Python Analysis Scripts

Python-based analysis tools for the controlled experiment energy consumption study.

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run Analysis
```bash
python analyze_energy_consumption.py
```

## 📊 Analysis Features

### **Energy Consumption Analysis**
- **Mode Comparison**: Energy usage across different chat modes
- **Token Efficiency**: Energy per token calculations
- **Distribution Analysis**: Energy consumption patterns
- **Statistical Summary**: Comprehensive metrics and statistics

### **Visualizations Generated**
- **Energy Consumption Chart**: Bar chart comparing modes
- **Token Efficiency Chart**: Energy per token and total tokens
- **Input/Output Scatter**: Token usage relationships
- **Energy Distribution**: Box plots showing consumption patterns

### **Output Files**
- **Charts**: High-resolution PNG files in `plots/` directory
- **Data**: CSV files with analysis results in `data/` directory
- **Reports**: Markdown reports in `reports/` directory

## 🔧 Usage

### **Basic Analysis**
```python
from analyze_energy_consumption import EnergyConsumptionAnalyzer

# Initialize analyzer
analyzer = EnergyConsumptionAnalyzer()

# Run complete analysis
analyzer.run_analysis()
```

### **Custom Analysis**
```python
# Load and preprocess data
analyzer = EnergyConsumptionAnalyzer()
analyzer.preprocess_data()

# Run specific analyses
energy_analysis = analyzer.analyze_energy_consumption()
efficiency_analysis = analyzer.analyze_token_efficiency()

# Create specific visualizations
analyzer.create_energy_consumption_chart()
analyzer.create_token_efficiency_chart()
```

## 📈 Key Metrics

### **Energy Metrics**
- **Total Energy**: Sum of all energy consumption
- **Average Energy per Prompt**: Mean energy consumption
- **Energy per Token**: Efficiency metric
- **Mode Comparison**: Relative energy usage

### **Token Metrics**
- **Input Tokens**: User prompt tokens
- **Output Tokens**: AI response tokens
- **Total Tokens**: Combined token usage
- **Input/Output Ratio**: Token efficiency

## 🎯 Research Applications

This analysis provides insights for:
- **Energy Efficiency Research**: Understanding AI energy consumption
- **Model Comparison**: Comparing different AI model efficiency
- **User Behavior Analysis**: How users interact with different modes
- **Sustainability Studies**: Environmental impact assessment

## 📋 Dependencies

- **pandas**: Data manipulation and analysis
- **matplotlib**: Plotting and visualization
- **seaborn**: Statistical data visualization
- **numpy**: Numerical computing
- **scipy**: Scientific computing
- **jupyter**: Interactive analysis (optional)

## 🔬 Methodology

### **Data Processing**
1. **Load JSON Data**: Import all experiment data files
2. **Data Cleaning**: Handle missing values and outliers
3. **Feature Engineering**: Calculate efficiency metrics
4. **Statistical Analysis**: Compute summary statistics

### **Visualization**
1. **Chart Creation**: Generate publication-ready plots
2. **Color Coding**: Consistent color scheme for modes
3. **Labeling**: Clear axis labels and titles
4. **Export**: High-resolution PNG files

### **Analysis Pipeline**
1. **Preprocessing**: Clean and validate data
2. **Aggregation**: Group by chat mode
3. **Calculation**: Compute efficiency metrics
4. **Visualization**: Create charts and plots
5. **Reporting**: Generate summary reports

## 📞 Support

For questions about the analysis or methodology, please refer to the main experiment documentation or create an issue in the repository.

---

**Part of sustainable AI research initiative** 🌱
