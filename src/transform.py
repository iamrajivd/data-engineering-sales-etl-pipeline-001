import csv
import json
from operator import add

def read_data(file_path):
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    print(f"Total Records reads: {len(data)}")
    return data

def clean_data(data):
    cleaned_data = []
    seen_ids = set()
    removed_count = 0

    for record in data:

        if not record['product']:
            removed_count += 1
            continue

        if not record['amount']:
            removed_count += 1
            continue

        if record['order_id'] in seen_ids:
            removed_count += 1
            continue

        record['amount'] = float(record['amount'])
    
        seen_ids.add(record['order_id'])

        cleaned_data.append(record)

    print(f"Records removed: {removed_count}")
    print(f"Records remaining: {len(cleaned_data)}")

    return cleaned_data

def transform_data(cleaned_data):
    product_summary = {}
    date_summary = {}

    for record in cleaned_data:
        product = record['product']
        amount = record['amount']
        date = record['date']

        if product in product_summary:
            product_summary[product] += amount
        else:
            product_summary[product] = amount

        if date in date_summary:
            date_summary[date] += amount
        else:
            date_summary[date] = amount
    
    top_product = max(product_summary, key=product_summary.get)

    print("Revenue per product:", product_summary)
    print("Revenue per date:", date_summary)
    print("Top Selling Product:", top_product)
    return product_summary, date_summary, top_product

def write_output(cleaned_data, product_summary, date_summary):

    with open("sales_cleaned.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=cleaned_data[0].keys())
        writer.writeheader()
        writer.writerows(cleaned_data)
    
    with open("product_summary.json", "w") as file:
        json.dump(product_summary, file, indent=4)

    with open("daily_summary.json", "w") as file:
        json.dump(date_summary, file, indent=4)

    print("Output files successfully created.")

if __name__ == "__main__":
    file_path = "/Users/iamrajivd/Documents/Leo_Rajiv_mini_Project_001/sales_raw.csv"  # Replace with your actual file path
    data = read_data(file_path)
    print(data[0])
    cleaned = clean_data(data)
    product_summary, date_summary, top_product = transform_data(cleaned)
    write_output(cleaned, product_summary, date_summary)

   
        