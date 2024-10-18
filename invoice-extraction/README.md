# Invoice Data Extraction Project

## Overview
This project focuses on extracting data from invoices (regular and scanned) in PDF format. It supports handling a variety of PDF types and ensures high accuracy in data extraction.


## Project Structure:

invoice-extraction/ │ ├── data/ │ ├── raw_data/ # Store raw PDF invoices │ ├── processed_data/ # Store extracted CSVs and other data formats │ └── actual_data/ # Store actual data for validation │ ├── notebooks/ │ └── invoice_extraction_analysis.ipynb # Jupyter notebooks for exploration and reports │ ├── src/ │ ├── init.py # Makes src a Python module │ ├── data_extraction.py # Text extraction from PDF files, including both regular and scanned PDFs │ ├── text_processing.py # Text parsing and extraction of specific fields using regular expressions │ ├── data_processing.py # Clean and process the extracted data │ ├── accuracy_evaluation.py # Evaluate the accuracy of the extracted data against actual │ ├── utils.py # Configuring paths or general utilities │ └── main.py # Handling overall workflow and initialization │ ├── requirements.txt # Project dependencies └── README.md # Project overview and instructions

## System Dependencies 
For Linux:

#!/bin/bash

Update system repositories
sudo apt-get update

Install Tesseract OCR
sudo apt-get install -y tesseract-ocr

Install Poppler-utils for pdf2image support
sudo apt-get install -y poppler-utils

For windows:

Tesseract OCR:**
   - Download the installer from the official Tesseract GitHub repository: [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - Run the installer and follow the prompts. Make sure to note the installation path as you will need to configure this path in your Python script to use `pytesseract`.

## Installation

To set up the project environment:

1. Clone this repository.
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the project by executing:

```bash
python main.py
```

## Dependencies
* PyMuPDF
* pytesseract
* pdf2image
* opencv-python
* pandas
* numpy

## Code Flow Explanation

### 1. `main.py` - Entry Point
- **Initialization**: The main script starts by calling the `process_invoices` function with a specified directory containing PDF invoices.
- **Data Processing**: After processing the invoices, the script loads and merges the extracted data with a actual dataset using `load_and_merge_data`.
- **Cleaning and Normalization**: The merged data is then passed through `apply_text_cleaning` to standardize the text format for accurate comparison.
- **Accuracy Evaluation**: Finally, the `evaluate_accuracy` function is called to assess how accurately the data was extracted compared to the actual. Results are printed to the console.

### 2. `data_extraction.py` - PDF Text Extraction
- **Text Extraction**: This module handles reading PDF files using `fitz` (PyMuPDF) and extracting text. If the PDF contains images (scanned PDF), `pdf2image` converts these to image format, and `pytesseract` is used to perform OCR (Optical Character Recognition).
- **Handling Multiple Files**: The `process_invoices` function iterates over all PDF files in a specified directory, applying text extraction to each and saving the results.

### 3. `text_processing.py` - Text Parsing
- **Regex Operations**: Extracted text is processed using regular expressions to find and isolate specific pieces of information like invoice numbers, dates, amounts, and customer details. This parsing logic is encapsulated in the `parse_invoice_data` function.

### 4. `data_processing.py` - Data Management
- **Data Loading**: This file contains functions to load the extracted data and the actual data from CSV files.
- **Data Merging and Cleaning**: It merges the two datasets based on common keys (e.g., Invoice Number)

### 5. `text_cleaning.py`- Text Cleaning
cleans the text fields to remove inconsistencies and prepare for accurate comparison.

### 6. `accuracy_evaluation.py` - Evaluation of Results
- **Accuracy Computation**: This script computes the accuracy for each field by comparing the cleaned and normalized extracted data against the cleaned and normalized actual. It handles both direct string comparison and fuzzy matching for fields where exact matches are not feasible (like complex bank details).

The flow of the program ensures that from the moment PDFs are read to the final accuracy reporting, every step is modular, making it easy to update specific parts without affecting others.


This `README.md` provides a clear overview of the project, its structure, installation steps, and how to use it.
