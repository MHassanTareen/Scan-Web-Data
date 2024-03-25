# Scan Web Data with MLT

This repository contains Python scripts designed for scanning and processing web data using Machine Learning Techniques (MLT). The scripts focus on data extraction, duplicate detection, and data storage functionalities.

## Contents

- **dataCheck.py**: This script provides functionality to check and preprocess data stored in Excel files. It includes features like detecting duplicate entries and replacing them with the latest ones.

- **scrapedata.py**: Responsible for web scraping using the BeautifulSoup library. It extracts data from a specified website, stores it in an Excel file, and allows for continuous scanning through pagination or "view more" links.

- **xleSave.py**: Contains utility functions for saving data to an Excel file and counting the number of entries in the Excel file.

## Usage

### dataCheck.py
Execute this script to check and preprocess data stored in Excel files. It provides commands for scanning, removing duplicates, and counting the number of entries.

### scrapedata.py
Use this script to scrape data from a website. After providing the initial URL, the script allows for continuous scanning through pagination or "view more" links.

### xleSave.py
Contains functions `saveToXle` and `count_data_entries` for saving data to an Excel file and counting the number of entries, respectively.

## How to Run

1. Clone the repository to your local machine:
   ```bash
   git clone <repository_url>
