import json
import csv,os
from urllib.parse import urlparse

# Updated CSV columns with new fields
csv_columns = [
    'sku', 'mpn', 'name', 'product_websites', 'attribute_set_code', 'product_type',
    'storage', 'condition', 'categories', 'price', 'qty', 'is_in_stock',
    'description', 'short_description', 'weight', 'visibility', 'tax_class_name',
    'meta_title', 'meta_description', 'meta_keyword', 'image', 'small_image',
    'thumbnail', 'brand', 'cpu_form_factor','cpu_socket','errors']

brands = {}
chipset = {}
cpu_socket = {}
cpu_form_factor = {}



mpns={}
processed_rows = []



def process_json_to_csv(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
        if isinstance(data, dict):
            data = [data]


    sku_counter = 40400  # For incremental SKU generation

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

        image_path = f"/motherboard/images/{part_no}.jpeg"  # New image path pattern
        parsed_url = urlparse(item.get('product_url', ''))
        full_image_url = f"{parsed_url.scheme}://{parsed_url.netloc}{image_path}" if parsed_url.netloc else ''
        old_file = os.path.join("C:\\Users\\Osaka Motors\\Desktop\\scripts\\scraping\\m4l\\motherboard\\images", f"{part_no}.jpeg")
        new_file = os.path.join("C:\\Users\\Osaka Motors\\Desktop\\scripts\\scraping\\m4l\\motherboard\\sku_images", f"{sku}.jpeg")
        
        try:
            os.rename(old_file,new_file)
        except:
            pass
        
        # os.rename(old_file,new_file)

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
            'meta_title': (item.get('title', '').replace('=',''))[:60],
            'meta_description': item.get('description', '').replace('N/A', ''),
            'meta_keyword': '',
            'image': f"{sku}.jpeg",
            'small_image': f"{sku}.jpeg",
            'thumbnail': f"{sku}.jpeg",
            'brand': specs.get('Manufacturer', '') if specs.get('Manufacturer', '') else '',
            'cpu_form_factor': specs.get('Form Factor', '') if specs.get('Form Factor', '') else '',
            'cpu_socket': specs.get('CPU Socket Type', '') if specs.get('CPU Socket Type', '') else '',
            'errors': ''
        }
                    
        if row['mpn'] not in mpns:
            mpns[row['mpn']] = sku
        else:
            row['sku'] = mpns[row['mpn']]
            row['image'] = f"{row['sku']}.jpeg"
            row['small_image'] = f"{row['sku']}.jpeg"
            row['thumbnail'] = f"{row['sku']}.jpeg"
            

        short_description = f"<ul> <li><strong>Part No. :</strong> {row['mpn']}</li>   <li><strong>Product Type:</strong> Motherboard</li>  "
        if row['brand'] != "NA":
            short_description += f"<li><strong>Brand :</strong> {row['brand']}</li> "
        row['short_description'] = f"{short_description}"

        
        if row['brand'] not in brands:
            brands[row['brand']] = 1
        else :
            brands[row['brand']] += 1

        # if row['Chipset'] not in chipset:
        #     chipset[row['Chipset']] = 1
        # else :
        #     chipset[row['Chipset']] += 1

        if row['cpu_socket'] not in cpu_socket:
            cpu_socket[row['cpu_socket']] = 1
        else :
            cpu_socket[row['cpu_socket']] += 1

        if row['cpu_form_factor'] not in cpu_form_factor:
            cpu_form_factor[row['cpu_form_factor']] = 1
        else :
            cpu_form_factor[row['cpu_form_factor']] += 1
            
        
        if row in processed_rows:
            print(f"Duplicate row found: {row['mpn']}")
            continue
        else:
            processed_rows.append(row)

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(processed_rows)

    sorted_chipset = dict(sorted(chipset.items(), key=lambda item: item[1], reverse=True))
    print(f"Chipset : {sorted_chipset}")

    sorted_cpu_socket = dict(sorted(cpu_socket.items(), key=lambda item: item[1], reverse=True))
    # print(f"Total Products : {len(processed_rows)}")
    print(f"Brands : {brands}")
    print(f"Chipset : {len(chipset)}")
    print(f"CPU Socket Type : {sorted_cpu_socket}")
    print(f"Form Factor : {cpu_form_factor}")

# Usage:
process_json_to_csv('motherboard/products.json', 'motherboard/motherboard.csv')