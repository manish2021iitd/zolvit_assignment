import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np
import pandas as pd
import os
import time
import re
from text_processing import parse_invoice_data
from config import OUTPUT_PATH

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file. If the PDF contains regular text, it returns the text as soon as it finds any.
    If the text extraction fails, it calls another function to handle scanned PDFs.

    Args:
        pdf_path (str): The path to the PDF file from which to extract text.

    Returns:
        str: The extracted text from the PDF or the result from the scanned PDF extraction function if the initial extraction fails.

    Raises:
        Prints an error message if an exception occurs during the extraction process.
    """
    try:
        with fitz.open(pdf_path) as pdf:
            for page_num in range(len(pdf)):
                page = pdf.load_page(page_num)
                text = page.get_text()
                if text.strip():
                    return text  # Regular PDF
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
    return extract_text_from_scanned_pdf(pdf_path)

def extract_text_from_scanned_pdf(pdf_path):
    """
    Extracts text from a scanned PDF by converting its pages to images and then applying optical character recognition (OCR).
    This function is typically called if the standard text extraction from `extract_text_from_pdf` fails.

    Args:
        pdf_path (str): The path to the scanned PDF file from which to extract text.

    Returns:
        str: A string containing the concatenated text extracted from each page of the scanned PDF.
    """
    images = convert_from_path(pdf_path)
    full_text = ""
    for image in images:
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(binary_image)
        full_text += text + "\n"
    return full_text


def process_invoice(pdf_path):
    """
    Processes a single invoice PDF by extracting text and parsing invoice data.

    Args:
        pdf_path (str): The path to the invoice PDF to process.

    Returns:
        dict: A dictionary containing key-value pairs of data fields extracted from the invoice.
    """
    text = extract_text_from_pdf(pdf_path)
    return parse_invoice_data(text)

def process_invoices(pdf_dir):
    """
    Processes all PDF invoices within a specified directory, extracts relevant invoice data, and saves the results to a CSV file.

    Args:
        pdf_dir (str): The directory path containing invoice PDF files.

    Outputs:
        Saves a CSV file with extracted data to a predefined output path. Prints the DataFrame before saving and the total processing time.
        
    Post-processing:
        Performs cleaning and formatting on certain fields to ensure data consistency and accuracy. For example, it removes commas from numerical fields and handles date formatting.
    """
    pdf_files = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    results = []
    start_time = time.time()
    for pdf_file in pdf_files:
        results.append(process_invoice(pdf_file))
    end_time = time.time()

    # Convert to DataFrame for easier handling
    df = pd.DataFrame(results)

    # Post-processing: Splitting 'Invoice Date' field to handle any extra text
    # Cleaning up fields if any additional unwanted text is found
    df['Invoice Date'] = df['Invoice Date'].apply(lambda x: x.split('\n')[0] if isinstance(x, str) else x)
    df['Due Date'] = df['Due Date'].apply(lambda x: x.split('\n')[0] if isinstance(x, str) else x)
    df['Taxable Amount'] = df['Taxable Amount'].str.replace(',', '').astype(float)
    df['Total'] = df['Total'].str.replace(',', '').astype(float)
    df['Bank Details'] = df['Bank Details'].apply(lambda x: re.sub(r'Bank:\n', '', x).strip() if isinstance(x, str) else x)
    
    print(df)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Total time taken to process all invoices: {end_time - start_time:.2f} seconds")
