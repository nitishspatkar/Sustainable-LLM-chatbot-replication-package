# User Survey Analysis

We provide files to analyze survey responses to understand user attitudes, usage patterns, and preferences regarding sustainable AI chatbot systems. The analysis combines traditional statistical methods with modern NLP techniques to extract insights from both structured and unstructured responses.


## Folder Structure

```
User-Survey/
├── Survey-Instrument/              # Survey design and questions
│   └── survey_questions.md         # Complete question definitions
├── Raw-Data/                       # Original survey data
│   └── data.xlsx                   # Survey responses (77 participants)
└── Analysis-Scripts/               # Python analysis code
    ├── src/                        # Source code modules
    ├── config/                     # Configuration files
    ├── requirements.txt            # Python dependencies
    └── output/                     # Generated results
        ├── plots/                  # Visualizations
        ├── data/                   # Processed data
        └── reports/                # Analysis reports
```

## Quick Start

### **Prerequisites**
```bash
# Python 3.8+ required
pip install -r requirements.txt
```

### **Run Analysis**
```bash
cd Analysis-Scripts
python src/analyze.py          # Generate all charts
python src/text_analysis.py    # Run NLP analysis
```

## Configuration

### **Chart Styling** (`config/chart_styles.yaml`)
- **Fonts**: Times New Roman, publication-ready sizes

### **Question Definitions** (`config/questions.yaml`)
- **Question mapping**: Column names to display titles
- **Scale definitions**: Likert scale configurations
- **Chart types**: Visualization specifications


## Dependencies

```
pandas==2.1.4
matplotlib==3.8.2
openpyxl==3.1.2
scikit-learn>=1.5.1
nltk>=3.9.1
PyYAML>=6.0
```

