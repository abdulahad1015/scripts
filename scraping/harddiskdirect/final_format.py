import json
import csv
from html_generator import generate_html  # Ensure this module is correctly implemented and available.

def write_json_to_csv(json_file, csv_file):
    """
    Writes specific data from a JSON file containing a list of dictionaries to a CSV file.

    Args:
        json_file (str): Path to the JSON file containing deduplicated data.
        csv_file (str): Path to the CSV file to be created.
    """
    # Load the JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Prepare the CSV fields
    csv_fields = [
        "Part No", "HTML"  # Technical Information and Generated HTML
    ]

    # Create the CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:

        writer = csv.DictWriter(file, fieldnames=csv_fields,quoting=csv.QUOTE_NONE,delimiter=',',quotechar='',escapechar='')     

        writer.writeheader()

        # Write each dictionary to the CSV file
        for item in data:
            # Initialize the row with top-level fields
            row = {}

            # Add General Information fields
            # general_info = item.get("General Information", {})
            # for key in ["Product Line", "Product Series", "Model", "OEM Manufacturer", "Product Type"]:
            #     row[key] = general_info.get(key, "")

            # # Add Technical Information fields
            # technical_info = item.get("Technical Information", {})
            # for key in ["# of Cores", "Processor Speed", "Socket Type"]:
            #     row[key] = technical_info.get(key, "")

            # Generate and add the HTML field
            row["HTML"] = f"'{generate_html(item)}'"

            # Write the row to the CSV
            # print(row)
            writer.writerow(row)

    print(f"Data successfully written to {csv_file}.")

# File paths
input_json = "deduplicated_data.json"  # Replace with your deduplicated JSON file path
output_csv = "processor_html.csv"  # Replace with your desired CSV file name

# Write JSON to CSV
write_json_to_csv(input_json, output_csv)



