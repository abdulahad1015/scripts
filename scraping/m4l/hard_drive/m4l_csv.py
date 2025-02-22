import json
import csv,os
from urllib.parse import urlparse

# Updated CSV columns with new fields
csv_columns = [
    'sku', 'mpn', 'name', 'product_websites', 'attribute_set_code', 'product_type',
    'storage', 'condition', 'categories', 'price', 'qty', 'is_in_stock',
    'description', 'short_description', 'weight', 'visibility', 'tax_class_name',
    'meta_title', 'meta_description', 'meta_keyword', 'image', 'small_image',
    'thumbnail', 'brand', 'hard_drive_type', 'hard_drive_capacity','hard_drive_bandwidth','hard_drive_pins','hard_drive_bus','hard_drive_error_correction','hard_drive_cycle_time','hard_drive_cas','hard_drive_rank','hard_drive_voltage' ,'errors'
]

brands = []
hard_drive_type = []
Capacity = []
Data_Transfer_Rate = []
Pins = []
Bus_Type = []
Error_Correction = []
Cycle_Time = []
Cas = []
Rank = []
Voltage = []
mpns={}
processed_rows = []


def process_json_to_csv(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
        if isinstance(data, dict):
            data = [data]


    sku_counter = 25150  # For incremental SKU generation

    for item in data:
        part_no = item.get('Part No', '')
        if part_no == 'NA':
            continue

        specs = item.get('specifications', {})
        description = "Specifications:\n <ul>"
        for i in specs:
            description += f"<li><strong>{i} :</strong> {specs[i]}</li>"
        description += "</ul>"

        # short_description = f"{specs.get('Brand', '') if specs.get('Brand', '') else ''}   
        # Generate incremental SKU
        sku = f"btd-{sku_counter:06d}"
        sku_counter += 1

        # Process image URL with part number
        part_no = part_no.replace('=','')

        image_path = f"/hard_drive/images/{part_no}.jpeg"  # New image path pattern
        parsed_url = urlparse(item.get('product_url', ''))
        full_image_url = f"{parsed_url.scheme}://{parsed_url.netloc}{image_path}" if parsed_url.netloc else ''

        old_file = os.path.join(r"C:\Users\Osaka Motors\Desktop\scripts\scraping\m4l\hard_drive\images", f"{part_no}.jpeg")
        new_file = os.path.join(r"C:\Users\Osaka Motors\Desktop\scripts\scraping\m4l\hard_drive\sku_images", f"{sku}.jpeg")

        # try:
        #     os.rename(old_file,new_file)
        # except:
        #     pass

        # Create row with new fields
        category='/'.join(filter(None, [
                item.get('category', ''),
                item.get('subcategory', ''),
                ]))
        

        row = {
            'sku': sku,
            'mpn': part_no,
            'name': item.get('title', ''),
            'product_websites': "base",
            'attribute_set_code': "Default",
            'product_type': 'simple',
            'storage': '',
            'condition': 'Used',
            'categories': f"Default Category/hard_drive/{category}",
            'price': item.get('price', '').replace('$', '').replace(',', ''),
            'qty': '5',
            'is_in_stock': '1',
            'description': f'{description}',
            'short_description': '',
            'visibility': 'Catalog, Search',
            'tax_class_name': 'Taxable Goods',
            'meta_title': item.get('title', '').replace('=',''),
            'meta_description': item.get('description', '').replace('N/A', ''),
            'meta_keyword': '',
            'image': f"{sku}.jpeg",
            'small_image': f"{sku}.jpeg",
            'thumbnail': f"{sku}.jpeg",
            'brand': specs.get('Manufacturer', '') if specs.get('Manufacturer', '') else '',
            'errors': ''
        }




                
        
        if row['mpn'] not in mpns:
            mpns[row['mpn']] = sku
        else:
            row['sku'] = mpns[row['mpn']]
            row['image'] = f"{row['sku']}.jpeg"
            row['small_image'] = f"{row['sku']}.jpeg"
            row['thumbnail'] = f"{row['sku']}.jpeg"
            

        short_description = f"<ul> <li><strong>Part No. :</strong> {row['mpn']}</li>   <li><strong>Product Type:</strong> hard_drive</li>  "
        if row['brand'] != "NA":
            short_description += f"<li><strong>Brand :</strong> {row['brand']}</li> "
        
        
        row['short_description'] = f"{short_description}"

        

        if row['brand'] not in brands:
            brands.append(row['brand'])
        if specs.get('hard_drive Type', '') not in hard_drive_type:
            hard_drive_type.append(specs.get('hard_drive Type', ''))
        if specs.get('Capacity', '') not in Capacity:
            Capacity.append(specs.get('Capacity', ''))
        if specs.get('Data Transfer Rate', '') not in Data_Transfer_Rate:
            Data_Transfer_Rate.append(specs.get('Data Transfer Rate', ''))
        if specs.get('Pins', '') not in Pins:
            Pins.append(specs.get('Pins', ''))
        # if specs.get('Bus Type', '') not in Bus_Type:
        #     Bus_Type.append(specs.get('Bus Type', ''))
        if specs.get('Error Correction', '') not in Error_Correction:
            Error_Correction.append(specs.get('Error Correction', ''))
        if specs.get('Cycle Time', '') not in Cycle_Time:
            Cycle_Time.append(specs.get('Cycle Time', ''))
        if specs.get('Cas', '') not in Cas:
            Cas.append(specs.get('Cas', ''))
        if specs.get('Rank', '') not in Rank:
            Rank.append(specs.get('Rank', ''))
        if specs.get('Voltage', '') not in Voltage:
            Voltage.append(specs.get('Voltage', ''))

        if row in processed_rows:
            print(f"Duplicate row found: {row['mpn']}")
            continue

        
        processed_rows.append(row)

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(processed_rows)

    print(f"Brands : {brands}")
    print(f"hard_drive Type : {hard_drive_type}")
    print(f"Capacity : {Capacity}")
    print(f"Data Transfer Rate : {Data_Transfer_Rate}")
    print(f"Pins : {Pins}")
    print(f"Bus Type : {Bus_Type}")
    print(f"Error Correction : {Error_Correction}")
    print(f"Cycle Time : {Cycle_Time}")
    print(f"Cas : {Cas}")
    print(f"Rank : {Rank}")
    print(f"Voltage : {Voltage}")
    print(f"Total Products : {len(processed_rows)}")


# Usage:
process_json_to_csv('hard_drive/products.json', 'hard_drive/hard_drive.csv')