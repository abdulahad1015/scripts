import json
import csv,os
from urllib.parse import urlparse

# Updated CSV columns with new fields
csv_columns = [
    'sku', 'mpn', 'name', 'product_websites', 'attribute_set_code', 'product_type',
    'storage', 'condition', 'categories', 'price', 'qty', 'is_in_stock',
    'description', 'short_description', 'weight', 'visibility', 'tax_class_name',
    'meta_title', 'meta_description', 'meta_keyword', 'image', 'small_image',
    'thumbnail', 'brand', 'processor_cores', 'processor_clock_speed', 'processor_socket', 'errors'
]

brands = []
sockets = []
cores = []
speeds = []
mpns={}


def process_json_to_csv(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
        if isinstance(data, dict):
            data = [data]

    processed_rows = []
    sku_counter = 1  # For incremental SKU generation

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
        image_path = f"/processors/images/{part_no}.jpeg"  # New image path pattern
        parsed_url = urlparse(item.get('product_url', ''))
        full_image_url = f"{parsed_url.scheme}://{parsed_url.netloc}{image_path}" if parsed_url.netloc else ''

        old_file = os.path.join(r"C:\Users\Osaka Motors\Desktop\scripts\scraping\m4l\processors\images", f"{part_no}.jpeg")
        new_file = os.path.join(r"C:\Users\Osaka Motors\Desktop\scripts\scraping\m4l\processors\sku_images", f"{sku}.jpeg")

        # try:
        #     os.rename(old_file,new_file)
        # except:
        #     pass

        # Create row with new fields
        category='/'.join(filter(None, [
                item.get('category', ''),
                item.get('subcategory', ''),
                item.get('brand', '')]))
        

        row = {
            'sku': sku,
            'mpn': part_no,
            'name': item.get('title', ''),
            'product_websites': "base",
            'attribute_set_code': "Default",
            'product_type': 'simple',
            'storage': '',
            'condition': 'Used',
            'categories': f"Default Category/CPUs/{category}",
            'price': item.get('price', '').replace('$', '').replace(',', ''),
            'qty': '1',
            'is_in_stock': '1',
            'description': f'{description}',
            'short_description': '',
            'weight': '',
            'visibility': 'Catalog, Search',
            'tax_class_name': 'Taxable Goods',
            'meta_title': item.get('title', ''),
            'meta_description': item.get('description', '').replace('N/A', ''),
            'meta_keyword': '',
            'image': f"{sku}.jpeg",
            'small_image': f"{sku}.jpeg",
            'thumbnail': f"{sku}.jpeg",
            'processor_cores': f"{specs.get('# of Cores', '')}-Core",
            'processor_clock_speed': specs.get('Clock Speed', ''),
            'processor_socket': specs.get('CPU Socket Type', ''),
            'errors': ''
        }

        if (row['processor_cores'] == '-Core') and (("Quad-Core"  in item.get('title', '') or "Quad Core" in item.get('title', '') or "4-Core" in item.get('title', '') or "4 Core" in item.get('title', ''))):  
            row['processor_cores'] = "4-Core"
        elif (row['processor_cores'] == '-Core') and (("Dual-Core"  in item.get('title', '') or "Dual Core" in item.get('title', '') or "2-Core" in item.get('title', '') or "2 Core" in item.get('title', ''))):
            row['processor_cores'] = "2-Core"
        elif (row['processor_cores'] == '-Core') and (("Hexa-Core"  in item.get('title', '') or "Hexa Core" in item.get('title', '') or "6-Core" in item.get('title', '') or "6 Core" in item.get('title', ''))):
            row['processor_cores'] = "6-Core"
        elif (row['processor_cores'] == '-Core') and (("Octa-Core"  in item.get('title', '') or "Octa Core" in item.get('title', '') or "8-Core" in item.get('title', '') or "8 Core" in item.get('title', ''))):
            row['processor_cores'] = "8-Core"
        elif (row['processor_cores'] == '-Core') and (("Deca-Core"  in item.get('title', '') or "Deca Core" in item.get('title', '') or "10-Core" in item.get('title', '') or "10 Core" in item.get('title', ''))):
            row['processor_cores'] = "10-Core"
        elif (row['processor_cores'] == '-Core') and (("Hexadeca-Core"  in item.get('title', '') or "Hexadeca Core" in item.get('title', '') or "16-Core" in item.get('title', '') or "16 Core" in item.get('title', ''))):
            row['processor_cores'] = "16-Core"
        elif (row['processor_cores'] == '-Core') and (("Triple-Core"  in item.get('title', '') or "Triple Core" in item.get('title', '') or "3-Core" in item.get('title', '') or "3 Core" in item.get('title', ''))):
            row['processor_cores'] = "3-Core"
        elif (row['processor_cores'] == '-Core') and (("Single-Core"  in item.get('title', '') or "Single Core" in item.get('title', '') or "1-Core" in item.get('title', '') or "1 Core" in item.get('title', ''))):
            row['processor_cores'] = "1-Core"

        if row['processor_cores'] == '-Core':
            row['processor_cores'] = 'NA'


        if specs.get('Manufacturer', ''):
            row['brand'] = specs.get('Manufacturer', '')
        elif specs.get('Brand', ''):
            row['brand'] = specs.get('Brand', '')
        else:
            if "Intel" in item.get('title', ''):
                row['brand'] = "Intel"
            elif "AMD" in item.get('title', ''):
                row['brand'] = "AMD"
            elif "HP" in item.get('title', ''):
                row['brand'] = "HP"
            elif "Dell" in item.get('title', ''):
                row['brand'] = "Dell"
            elif "IBM" in item.get('title', ''):
                row['brand'] = "IBM"
            elif "Lenovo" in item.get('title', ''):
                row['brand'] = "Lenovo"
            elif "Fujitsu" in item.get('title', ''):
                row['brand'] = "Fujitsu"
            elif "Sun" in item.get('title', ''):
                row['brand'] = "Sun"
            elif "Toshiba" in item.get('title', ''):
                row['brand'] = "Toshiba"
            else:
                row['brand'] = "NA"
                
        
        if row['mpn'] not in mpns:
            mpns[row['mpn']] = sku
        else:
            row['sku'] = mpns[row['mpn']]

        short_description = f"<ul> <li><strong>Part No. :</strong> {row['mpn']}</li>   <li><strong>Product Type:</strong> CPU/Microprocessor</li>  "
        if row['brand'] != "NA":
            short_description += f"<li><strong>Brand :</strong> {row['brand']}</li> "
        if row['processor_cores'] != "":
            short_description += f"<li><strong>Processor Cores :</strong> {row['processor_cores']}</li> "
        
        row['short_description'] = f"{short_description}"

        

        if row['brand'] not in brands:
            brands.append(row['brand'])
        if row['processor_cores'] not in cores:
            cores.append(row['processor_cores'])
        if row['processor_clock_speed'] not in speeds:
            speeds.append(row['processor_clock_speed'])
        if row['processor_socket'] not in sockets:
            sockets.append(row['processor_socket'])
        
        processed_rows.append(row)

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(processed_rows)

    print(f"Brands : {brands}")
    print(f"Cores : {cores}")
    print(f"Speeds : {speeds}")
    print(f"Sockets : {sockets}")

# Usage:
process_json_to_csv('processors/processors.json', 'processors/processors.csv')