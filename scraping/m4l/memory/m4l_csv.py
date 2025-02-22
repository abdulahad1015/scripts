import json
import csv,os
from urllib.parse import urlparse

# Updated CSV columns with new fields
csv_columns = [
    'sku', 'mpn', 'name', 'product_websites', 'attribute_set_code', 'product_type',
    'storage', 'condition', 'categories', 'price', 'qty', 'is_in_stock',
    'description', 'short_description', 'weight', 'visibility', 'tax_class_name',
    'meta_title', 'meta_description', 'meta_keyword', 'image', 'small_image',
    'thumbnail', 'brand', 'memory_type', 'memory_capacity','memory_bandwidth','memory_pins','memory_bus','memory_error_correction','memory_cycle_time','memory_cas','memory_rank','memory_voltage' ,'errors'
]

brands = []
memory_type = []
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


    sku_counter = 13470  # For incremental SKU generation

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

        image_path = f"/memory/images/{part_no}.jpeg"  # New image path pattern
        parsed_url = urlparse(item.get('product_url', ''))
        full_image_url = f"{parsed_url.scheme}://{parsed_url.netloc}{image_path}" if parsed_url.netloc else ''

        old_file = os.path.join(r"C:\Users\Osaka Motors\Desktop\scripts\scraping\m4l\memory\images", f"{part_no}.jpeg")
        new_file = os.path.join(r"C:\Users\Osaka Motors\Desktop\scripts\scraping\m4l\memory\sku_images", f"{sku}.jpeg")

        try:
            os.rename(old_file,new_file)
        except:
            pass

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
            'categories': f"Default Category/Memory/{category}",
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
            'memory_type': specs.get('Memory Type', '') if specs.get('Memory Type', '') else '',
            'memory_capacity': specs.get('Capacity', '') if specs.get('Capacity', '') else '',
            'memory_bandwidth': specs.get('Data Transfer Rate', '') if specs.get('Data Transfer Rate', '') else '',
            'memory_pins': specs.get('Pins', '') if specs.get('Pins', '') else '',
            'memory_bus': specs.get('Bus Type', '') if specs.get('Bus Type', '') else '',
            'memory_error_correction': specs.get('Error Correction', '') if specs.get('Error Correction', '') else '',
            'memory_cycle_time': specs.get('Cycle Time', '') if specs.get('Cycle Time', '') else '',
            'memory_cas': specs.get('Cas', '') if specs.get('Cas', '') else '',
            'memory_rank': specs.get('Rank', '') if specs.get('Rank', '') else '',
            'memory_voltage': specs.get('Voltage', '') if specs.get('Voltage', '') else '',
            'errors': ''
        }




                
        
        if row['mpn'] not in mpns:
            mpns[row['mpn']] = sku
        else:
            row['sku'] = mpns[row['mpn']]
            row['image'] = f"{row['sku']}.jpeg"
            row['small_image'] = f"{row['sku']}.jpeg"
            row['thumbnail'] = f"{row['sku']}.jpeg"
            

        short_description = f"<ul> <li><strong>Part No. :</strong> {row['mpn']}</li>   <li><strong>Product Type:</strong> Memory</li>  "
        if row['brand'] != "NA":
            short_description += f"<li><strong>Brand :</strong> {row['brand']}</li> "
        
        
        row['short_description'] = f"{short_description}"

        

        if row['brand'] not in brands:
            brands.append(row['brand'])
        if specs.get('Memory Type', '') not in memory_type:
            memory_type.append(specs.get('Memory Type', ''))
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
    print(f"Memory Type : {memory_type}")
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
process_json_to_csv('memory/products.json', 'memory/memory.csv')