from fuzzywuzzy import fuzz

# Evaluate accuracy for each field (excluding Bank Details, which uses fuzzy matching)
def evaluate_accuracy(merged):
    """
    Evaluates the accuracy of each field in a merged DataFrame and applies fuzzy matching to the 'Bank Details' field.

    This function calculates the accuracy for several fields based on exact matches between cleaned 'true' and 'predicted' values. It specifically uses fuzzy matching for the 'Bank Details' field to account for minor discrepancies in string values and logs details for entries with low similarity scores.

    Args:
        merged (DataFrame): A DataFrame that contains the merged 'true' and 'predicted' data for various fields.

    Processes:
        - Computes accuracy for standard fields ('Invoice Date', 'Due Date', 'Customer Details', 'Place of Supply', 'Taxable Amount', 'Total', 'Total Discount') by comparing the exact string matches of the cleaned data.
        - Uses fuzzy matching for the 'Bank Details' field to determine the similarity percentage between the true and predicted strings, applying a threshold to log discrepancies.
        - Outputs accuracy metrics for each field and logs specific cases where the 'Bank Details' similarity is below a set threshold.

    Outputs:
        - Prints the accuracy for each field.
        - Logs discrepancies in 'Bank Details' with similarity below 90% for further debugging.
        - Calculates and prints the overall accuracy for 'Bank Details' based on a predefined similarity threshold (e.g., 95%).
    """
    for field in ['Invoice Date', 'Due Date', 'Customer Details', 'Place of Supply', 'Taxable Amount', 'Total', 'Total Discount']:
        y_true_column = f'{field}_true_clean'
        y_pred_column = f'{field}_pred_clean'

        if y_true_column in merged.columns and y_pred_column in merged.columns:
            y_true = merged[y_true_column]
            y_pred = merged[y_pred_column]
            
            accuracy = (y_true == y_pred).sum() / len(y_true)
            print(f'Accuracy for {field}: {accuracy:.2f}')
        else:
            print(f"Column '{field}' not found in merged DataFrame")

    # Fuzzy matching for 'Bank Details'
    merged['Bank_Details_similarity'] = merged.apply(lambda row: fuzz.ratio(row['Bank Details_true_clean'], row['Bank Details_pred_clean']), axis=1)

    # Log discrepancies for debugging
    for index, row in merged.iterrows():
        if row['Bank_Details_similarity'] < 90:  # Log only low similarity cases
            print(f"\nInvoice {row['Invoice Number']}")
            print(f"True Bank Details: {row['Bank Details_true_clean']}")
            print(f"Pred Bank Details: {row['Bank Details_pred_clean']}")
            print(f"Similarity: {row['Bank_Details_similarity']}")

    # Set threshold for acceptable similarity (e.g., 95%)
    similarity_threshold = 95
    bank_details_accuracy = (merged['Bank_Details_similarity'] >= similarity_threshold).sum() / len(merged)

    print(f'Accuracy for Bank Details: {bank_details_accuracy:.2f}')

    print("evaluate_accuracy done")

