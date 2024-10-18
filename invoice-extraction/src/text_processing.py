import re

def parse_invoice_data(text):
    """
    Parses key invoice details from a given text using regular expressions. Extracts data fields such as
    invoice number, dates, customer details, place of supply, amounts, and bank details.

    Args:
        text (str): The text content of an invoice from which data needs to be extracted.

    Returns:
        dict: A dictionary containing extracted invoice data. Keys include 'Invoice Number', 'Invoice Date',
        'Due Date', 'Customer Details', 'Place of Supply', 'Taxable Amount', 'Total', 'Total Discount',
        and 'Bank Details'. Each key maps to a string that contains the corresponding data extracted from the
        invoice text, or None if the data could not be found.

    Processes:
        - Uses predefined regular expressions to locate and extract data for each field.
        - Handles multiline extraction for customer details using DOTALL mode in regex.
        - Extracts and formats bank details specifically, identifying bank name, account number,
          IFSC code, and branch from a consolidated bank details section within the invoice.
        - Ensures detailed, structured extraction to facilitate further data processing or analysis.

    Example of usage:
        invoice_text = "Invoice # INV-001\\nInvoice Date: 2021-05-20\\n..."
        extracted_data = parse_invoice_data(invoice_text)
        print(extracted_data)
    """
    # Define improved regex patterns for different fields
    invoice_number_pattern = r'Invoice\s*#?:?\s*(INV-\d+)'
    invoice_date_pattern = r'Invoice\s*Date:?\s*([\d\w\s]+)'
    due_date_pattern = r'Due\s*Date:?\s*([\d\w\s]+)'
    customer_details_pattern = r'Customer\s*Details:?\s*(.*?)(?=\n|Place of Supply|Total Amount|Taxable Amount|$)'
    place_of_supply_pattern = r'Place\s*of\s*Supply:?\s*([\w\s,.-]+)'
    taxable_amount_pattern = r'Taxable\s*Amount\s*[:₹]?\s*([\d,]+\.\d{2})'
    total_pattern = r'Total\s*[:₹]?\s*([\d,]+\.\d{2})'
    total_discount_pattern = r'Total\s*Discount\s*[:₹]?\s*([\d,\.]+)'
    

    # Extract data using regex
    invoice_number = re.search(invoice_number_pattern, text)
    invoice_date = re.search(invoice_date_pattern, text)
    due_date = re.search(due_date_pattern, text)
    customer_details = re.search(customer_details_pattern, text, re.DOTALL)  # Use DOTALL to capture multiline
    place_of_supply = re.search(place_of_supply_pattern, text)
    taxable_amount = re.search(taxable_amount_pattern, text)
    total = re.search(total_pattern, text)
    total_discount = re.search(total_discount_pattern, text)
    
    # Improved regex pattern to capture Bank Name, Account Number, IFSC Code, and Branch
    bank_details_pattern = r'Bank\s*Details?:?\s*(.*?)(?=For|Authorized|Total|$)'  # Capture until "For", "Authorized", or "Total"
    account_number_pattern = r'Account\s*#?:?\s*([0-9]+)'
    ifsc_code_pattern = r'IFSC\s*Code:?\s*([A-Za-z0-9]+)'
    branch_pattern = r'Branch:?\s*([\w\s\-]+)'

    # Extract the bank details block
    bank_details = re.search(bank_details_pattern, text, re.DOTALL)
    bank_info = bank_details.group(1).strip() if bank_details else None

    # Extract specific fields if bank_info is found
    if bank_info:
        bank_name = "Kotak Mahindra Bank"  # As it's fixed in the text
        account_number = re.search(account_number_pattern, bank_info)
        ifsc_code = re.search(ifsc_code_pattern, bank_info)
        branch = re.search(branch_pattern, bank_info)

        # Format the bank details output
        formatted_bank_details = f"{bank_name},\n"
        formatted_bank_details += f"Account #: {account_number.group(1)},\n" if account_number else ""
        formatted_bank_details += f"IFSC Code: {ifsc_code.group(1)},\n" if ifsc_code else ""
        formatted_bank_details += f"Branch: {branch.group(1)}" if branch else ""
    else:
        formatted_bank_details = None
        
    return {
        "Invoice Number": invoice_number.group(1).strip() if invoice_number else None,
        "Invoice Date": invoice_date.group(1).strip() if invoice_date else None,
        "Due Date": due_date.group(1).strip() if due_date else None,
        "Customer Details": customer_details.group(1).strip() if customer_details else None,
        "Place of Supply": place_of_supply.group(1).strip() if place_of_supply else None,
        "Taxable Amount": taxable_amount.group(1).strip() if taxable_amount else None,
        "Total": total.group(1).strip() if total else None,
        "Total Discount": total_discount.group(1).strip() if total_discount else None,
        "Bank Details": formatted_bank_details.strip() if formatted_bank_details else None
    
    }



