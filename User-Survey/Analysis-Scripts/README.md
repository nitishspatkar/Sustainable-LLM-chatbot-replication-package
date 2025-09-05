# Survey Analyzer


## Project Structure

```
survey analyzer/
├── config/                          # Configuration files
│   ├── chart_styles.yaml           # Styling parameters
│   └── questions.yaml              # Question definitions
├── src/
│   ├── utils/                      # Utility modules
│   │   ├── styling.py              # Chart styling management
│   │   ├── file_manager.py         # Output organization
│   │   └── config_loader.py        # Configuration loading
│   ├── visualization/              # Chart classes
│   │   └── base.py                 # Base chart functionality
│   ├── analyze.py                  # Main analysis script
│   ├── visualize.py                # Chart creation functions
│   └── text_analysis.py            # NLP analysis
├── data/
│   └── data.xlsx                   # Survey data
├── output/                         # Generated outputs
│   ├── plots/                      # Visualizations
│   │   ├── demographics/           # Demographics charts
│   │   ├── environmental/          # Environmental charts
│   │   │   ├── individual/         # Single question charts
│   │   │   ├── grouped/            # Multi-question charts
│   │   │   └── combined/           # All-in-one charts
│   │   └── usage/                  # Usage pattern charts
│   ├── data/                       # Processed data files
│   └── reports/                    # Analysis reports
└── README.md
```


### Prerequisites
- Python 3.8+
- Required packages (see requirements.txt)

### Installation
```bash
# Clone or download the project
cd survey-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the analysis
python src/analyze.py

# Run text analysis
python src/text_analysis.py
```
