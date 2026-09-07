price_patterns_model_tests

Background

price_patterns_model_tests is a quantitative finance research project designed to analyse historical stock-price data and investigate patterns in price movements over time.

The project currently includes analysis such as:

- Moving averages
- Monthly descriptive statistics
- Daily and log returns
- Rolling volatility
- Price Z-scores
- Mean-reversion indicators
- Geometric Brownian Motion
- Monte Carlo simulations
- Other stochastic-process-based analysis

The aim of the project is to explore how mathematical and statistical techniques can be applied to historical financial data and to build a reusable framework for quantitative research.

Repository

Clone the repository using:

git clone https://github.com/Emmanuel-Quant-Dev/price_patterns_model_tests.git

Then navigate into the project:

cd price_patterns_model_tests

Requirements

Python must be installed on your machine.

It is recommended to create a virtual environment before installing the project dependencies:

python3 -m venv env

Activate the environment on macOS/Linux:

source env/bin/activate

Then install the required Python packages:

pip install -r requirements.txt

Stock Data

Historical stock CSV files are stored inside:

data/list_of_stocks/stocks/

For example:

data/
└── list_of_stocks/
└── stocks/
├── AA.csv
├── AAPL.csv
├── MSFT.csv
└── ...

The expected CSV structure is:

Date,Open,High,Low,Close,Adj Close,Volume

Before running the analysis, configure run_play.py to use one of the CSV files available in the data/list_of_stocks/stocks/ directory.

For example:

stock = "AA.csv"

The value must correspond to an existing CSV file in the stock-data directory.

How to Execute

Once the stock has been selected, run:

python3 run_play.py

The script will execute the available quantitative-analysis modules against the selected historical stock dataset.

Generated analysis files are written to the:

results/

directory.

Depending on the analysis being run, outputs can include:

results/
├── AA_quant_analysis.csv
├── AA_monthly_statistics.csv
├── AA_monthly_return_statistics.csv
├── AA_monthly_price_range.csv
├── AA_stochastic_analysis.csv
├── AA_monthly_stochastic_statistics.csv
├── AA_monte_carlo_summary.csv
├── AA_probability_summary.csv
└── AA_gbm_simulations.csv

Project Structure

price_patterns_model_tests/
│
├── data/
│ └── list_of_stocks/
│ └── stocks/
│ └── historical stock CSV files
│
├── moving_averages/
│ └── moving_averages.py
│
├── stochastic_process/
│ └── stochastic_process.py
│
├── results/
│ └── generated analysis files
│
├── run_play.py
│
├── requirements.txt
│
└── README.md

Disclaimer

This project is intended for educational and quantitative-research purposes only.
