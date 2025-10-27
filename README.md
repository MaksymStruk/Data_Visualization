# Data Visualization by Region and Macroregion

This project allows you to visualize regional and macroregional data from a CSV file using interactive bar charts with color gradients.  

## Features
- View value distribution for individual regions.
- Compare average values across regions in a macroregion.
- Compare average values across all regions.
- Color gradient bars with an interactive colorbar.
- Saves generated charts as PNG files.

## Requirements
- Python 3.8+
- pandas
- matplotlib
- numpy

## Install dependencies with:

```bash
pip install pandas matplotlib numpy
```

## File Structure
```
project/
├─ data/
│   └─ input_data.csv       # Input data file
├─ macroregions.py          # Dictionary with macroregion definitions
├─ main.py                  # Main script with plotting functions
└─ results/                 # Folder where charts are saved
```

## CSV Format

The CSV file should contain three columns:

| Область | Місто/Район | Значення |
|--------|---------------|-------|
| Львівська   | м. Львів          | 985   |

## How to Run

Run the main script:

```bash
python main.py
```