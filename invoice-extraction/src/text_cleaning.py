import re

def clean_text(text, case='lower'):
    """
    Cleans and normalizes text according to specified casing rules. This function removes extra spaces and
    newline characters, and can convert text to lower case, title case, or leave it as is based on the
    'case' parameter. Additional specific substrings can also be removed during the process.

    Args:
        text (str): The text to be cleaned.
        case (str): Determines the text case transformation:
                    'lower' for lowercasing all characters,
                    'title' for capitalizing the first letter of each word.
                    Default is 'lower'.

    Returns:
        str: The cleaned and case-normalized text. If the input is not a string, returns the input unchanged.

    Example:
        input_text = " Here is some Text that needs Cleaning    "
        clean_text(input_text, case='title')
        # Output: "Here Is Some Text That Needs Cleaning"
    """
    if isinstance(text, str):
        cleaned = ' '.join(text.strip().split())  # Removes extra spaces and newlines
        if case == 'lower':
            cleaned = cleaned.lower()  # Normalize case to lower
        elif case == 'title':
            cleaned = cleaned.title()  # Normalize case to title (first letter capitalized)
        # Remove specific extra text that appears in Bank Details
        cleaned = re.sub(r'uncue dermacare pvt ltd', '', cleaned).strip()
        return cleaned
    return text

def apply_cleaning(merged):
    """
    Applies text cleaning to all relevant fields in a DataFrame using the `clean_text` function. 
    It also normalizes the case of the text based on the field, specifically setting the 'Customer Details'
    field to title case and others to lower case.

    Args:
        merged (DataFrame): The DataFrame containing the fields to be cleaned. Each field should have 'true'
        and 'pred' versions (e.g., 'Customer Details_true' and 'Customer Details_pred').

    Returns:
        DataFrame: The modified DataFrame with cleaned fields. Updates are made directly to columns such as
        '[field]_true_clean' and '[field]_pred_clean'.

    Additional Processing:
        - Handles NaN values in the 'Total Discount_pred_clean' field by replacing them with 0.0 for consistency in comparisons.

    Note:
        Prints a success message upon completion of cleaning operations.
    """
    # Apply cleaning function to all fields, normalizing "Customer Details" to title case
    for field in ['Invoice Date', 'Due Date', 'Customer Details', 'Place of Supply', 'Taxable Amount', 'Total', 'Total Discount', 'Bank Details']:
        case_setting = 'title' if field == 'Customer Details' else 'lower'
        merged[f'{field}_true_clean'] = merged[f'{field}_true'].apply(lambda x: clean_text(x, case=case_setting))
        merged[f'{field}_pred_clean'] = merged[f'{field}_pred'].apply(lambda x: clean_text(x, case=case_setting))

    # Handle NaN values in 'Total Discount' by replacing NaN with 0.0 for comparison
    merged['Total Discount_pred_clean'] = merged['Total Discount_pred_clean'].fillna(0.0)


    print("Text in merged data cleaned successfully")
    return merged
