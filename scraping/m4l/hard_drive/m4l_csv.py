import json
import csv,os
from urllib.parse import urlparse

# Updated CSV columns with new fields
csv_columns = [
    'sku', 'mpn', 'name', 'product_websites', 'attribute_set_code', 'product_type',
    'storage', 'condition', 'categories', 'price', 'qty', 'is_in_stock',
    'description', 'short_description', 'weight', 'visibility', 'tax_class_name',
    'meta_title', 'meta_description', 'meta_keyword', 'image', 'small_image',
    'thumbnail', 'brand', 'hard_drive_interface','hard_drive_capacity' ,'hard_drive_speed','hard_drive_form_factor','hard_drive_cache','errors'
]

brands = []



mpns={}
processed_rows = []
hard_drive_interface = []
hard_drive_speed = []
hard_drive_form_factor = []
hard_drive_cache = []
Capacity = {}


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
        old_file = os.path.join("C:\\Users\\Osaka Motors\\Desktop\\scripts\\scraping\\m4l\\hard_drive\\images", f"{part_no}.jpeg")
        new_file = os.path.join("C:\\Users\\Osaka Motors\\Desktop\\scripts\\scraping\\m4l\\hard_drive\\sku_images", f"{sku}.jpeg")
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
            'meta_title': item.get('title', '').replace('=',''),
            'meta_description': item.get('description', '').replace('N/A', ''),
            'meta_keyword': '',
            'image': f"{sku}.jpeg",
            'small_image': f"{sku}.jpeg",
            'thumbnail': f"{sku}.jpeg",
            'brand': specs.get('Manufacturer', '') if specs.get('Manufacturer', '') else '',
            'hard_drive_interface': specs.get('Drive Interface Type', '') if specs.get('Drive Interface Type', '') else '',
            'hard_drive_speed': specs.get('Spindle Speed', '') if specs.get('Spindle Speed', '') else '',
            'hard_drive_form_factor': specs.get('Form Factor', '') if specs.get('Form Factor', '') else '',
            'hard_drive_cache': specs.get('Cache', '') if specs.get('Cache', '') else '',
            'hard_drive_capacity': specs.get('Capacity', '') if specs.get('Capacity', '') else '',

            'errors': ''
        }
        capacity = row['hard_drive_capacity']
        if capacity:
            value = int(float(capacity.split()[0]))
            unit = capacity.split()[-1]
            if (unit == "MB") or (unit=="GB" and value <= 9):
                row['hard_drive_capacity']="500MB - 10GB"
            elif (unit == "GB" and value <= 20):
                row['hard_drive_capacity']="10GB - 20GB"
            elif (unit == "GB" and value <= 40):
                row['hard_drive_capacity']="20GB - 40GB"
            elif (unit == "GB" and value <= 80):
                row['hard_drive_capacity']="40GB - 80GB"
            elif (unit == "GB" and value <= 160):
                row['hard_drive_capacity']="80GB - 160GB"
            elif (unit == "GB" and value <= 320):
                row['hard_drive_capacity']="160GB - 320GB"
            elif (unit == "GB" and value <= 500):
                row['hard_drive_capacity']="320GB - 500GB"
            elif (unit == "GB" and value < 1000):
                row['hard_drive_capacity']="500GB - 1TB"
            else:
                row['hard_drive_capacity']=f"{value} {unit}"
            

                
        
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
        if row['hard_drive_interface'] not in hard_drive_interface:
            hard_drive_interface.append(row['hard_drive_interface'])
        if row['hard_drive_speed'] not in hard_drive_speed:
            hard_drive_speed.append(row['hard_drive_speed'])
        if row['hard_drive_form_factor'] not in hard_drive_form_factor:
            hard_drive_form_factor.append(row['hard_drive_form_factor'])
        if row['hard_drive_cache'] not in hard_drive_cache:
            hard_drive_cache.append(row['hard_drive_cache'])

        
        
        if row['hard_drive_capacity'] not in Capacity:
            Capacity[row['hard_drive_capacity']]=1
        else:
            Capacity[row['hard_drive_capacity']]+=1
            # Capacity.append(row['hard_drive_capacity'])
        

        if row in processed_rows:
            print(f"Duplicate row found: {row['mpn']}")
            continue

        
        processed_rows.append(row)

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(processed_rows)

    keys_to_remove = [key for key, value in Capacity.items() if value < 5]
    for key in keys_to_remove:
        Capacity.pop(key)
    sorted_capacity = dict(sorted(Capacity.items(), key=lambda item: item[1], reverse=True))
    print(f"Capacity : {Capacity}")

    print(f"Brands : {brands}")
    print(f"Capacity : {sorted_capacity}")
    print(f"Hard Drive Interface : {hard_drive_interface}")
    print(f"Hard Drive Speed : {hard_drive_speed}")
    print(f"Hard Drive Form Factor : {hard_drive_form_factor}")
    print(f"Hard Drive Cache : {hard_drive_cache}")





    print(f"Total Products : {len(processed_rows)}")


# Usage:
process_json_to_csv('hard_drive/products.json', 'hard_drive/hard_drive.csv')