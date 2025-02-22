import json

def find_common_specifications(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    common_keys = None

    for line in lines:
        product = json.loads(line)
        specifications = product.get("specifications", {})
        keys = set(specifications.keys())

        if common_keys is None:
            common_keys = keys
        else:
            common_keys &= keys

    return common_keys

if __name__ == "__main__":
    file_path = "/c:/Users/Osaka Motors/Desktop/scripts/scraping/m4l/memory/products.json"
    common_specifications = find_common_specifications(file_path)
    print("Common specifications fields:", common_specifications)
