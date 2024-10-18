from data_extraction import process_invoices
from data_processing import load_data, merge_data
from text_cleaning import apply_cleaning
from accuracy_evaluation import evaluate_accuracy
from config import TESSERACT_PATH, PDF_FILES_PATH, ACTUAL_DATA_PATH,OUTPUT_PATH

import pytesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def main():
    # Process PDF invoices
    process_invoices(PDF_FILES_PATH)

    # Load  actual data and extracted data
    actual_data  = load_data(ACTUAL_DATA_PATH)
    #print(actual_data)
    
    extracted_data = load_data(OUTPUT_PATH)
    #print(extracted_data)

    # merge actual data and extracted data
    merged = merge_data(actual_data, extracted_data)
    #print(merged)

    # Clean and normalize text fields of merged data
    clean_data = apply_cleaning(merged)
    #print(clean_data)

    # Evaluate and print the accuracy
    evaluate_accuracy(clean_data)
    

if __name__ == "__main__":
    main()
