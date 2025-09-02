# LLM Survey Analyzer

A Python-based tool for analyzing and visualizing survey data about LLM (Large Language Model) chatbot usage patterns.

## Project Structure
```
.
├── data/               # Data directory
│   └── data.xlsx      # Survey response data
├── src/               # Source code
│   ├── visualize.py   # Visualization functions
│   └── analyze.py     # Data analysis functions
├── output/            # Generated visualizations
│   └── plots/         # Plot images
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your survey data Excel file in the `data/` directory
2. Run the analysis:
```bash
python src/analyze.py
```

The script will generate visualizations in the `output/plots/` directory.

## Dependencies

- pandas==2.1.4
- matplotlib==3.8.2
- openpyxl==3.1.2 