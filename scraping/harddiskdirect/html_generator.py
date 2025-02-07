import json

data = {
    "Part No": "512207-800",
    "Brand": " HP ",
    "Category": "Processors",
    "sub_category": "Laptop Processors",
    "sub_sub_category": "NA",
    "Title": "512207-800 - HP 2.53GHz BGA479 Core 2 Duo P8700 2-Core Processor",
    "Description": "HP 512207-800 2.53GHz 1066MHz FSB 3MB L2 Cache Socket BGA479 Intel Core 2 Duo P8700 Dual-core (2 Core) Processor",
    "Condition": "Refurbished",
    "Price": "$69.00",
    "Image": "https://cdn.cmshardware.com/images/Images/Products/512207-800.webp",
    "General Information": {
        "Product Line": "Core 2 Duo ",
        "Model": "P8700  ",
        "Product Type": "Micro Processor ",
        "OEM Manufacturer": "HP "
    },
    "Technical Information": {
        "# of Cores": "Dual-core (2 Core) ",
        "Processor Speed": "2.53 GHz",
        "FSB": "1066 MHz",
        "Level 2 Cache Memory": "3 MB",
        "Processor Bit": "64-bit ",
        "lithography": "45 nm",
        "Thermal Power": "25 Watts",
        "Thermal Specification": "105 °C"
    },
    "Miscellaneous": {
        "Assembly Required": "Yes ",
        "Eco Friendly": "Yes "
    }
}

def generate_html(data):
    html = []

    # Adding product title and image
    html.append('<div _ngcontent-serverapp-c3289205036="" class="tab_body ng-star-inserted">')
    html.append(f'  <div _ngcontent-serverapp-c3289205036="" class="tablecustom ng-star-inserted">')
    html.append(f'    <div _ngcontent-serverapp-c3289205036="" class="ng-star-inserted">')
    html.append(f'      <p _ngcontent-serverapp-c3289205036="" class="headtable">General Information</p>')

    # General Information
    for key, value in data["General Information"].items():
        html.append(f'      <div _ngcontent-serverapp-c3289205036="" class="tablerow ng-star-inserted">')
        html.append(f'        <div _ngcontent-serverapp-c3289205036="" class="tablecolumn">')
        html.append(f'          <span _ngcontent-serverapp-c3289205036="" class="attribute-title">{key}</span>')
        html.append(f'        </div>')
        html.append(f'        <div _ngcontent-serverapp-c3289205036="" class="tablecolumn">')
        html.append(f'          <div _ngcontent-serverapp-c3289205036="" class="attribute-value">')
        html.append(f'            <span _ngcontent-serverapp-c3289205036="" class="multiattribute ng-star-inserted">{value}</span>')
        html.append(f'          </div>')
        html.append(f'        </div>')
        html.append(f'      </div>')

    html.append(f'    </div>')
    html.append(f'  </div>')
 
    # Adding Technical Information section
    html.append(f'  <div _ngcontent-serverapp-c3289205036="" class="tablecustom ng-star-inserted">')
    html.append(f'    <div _ngcontent-serverapp-c3289205036="" class="ng-star-inserted">')
    html.append(f'      <p _ngcontent-serverapp-c3289205036="" class="headtable">Technical Information</p>')

    for key, value in data["Technical Information"].items():
        html.append(f'      <div _ngcontent-serverapp-c3289205036="" class="tablerow ng-star-inserted">')
        html.append(f'        <div _ngcontent-serverapp-c3289205036="" class="tablecolumn">')
        html.append(f'          <span _ngcontent-serverapp-c3289205036="" class="attribute-title">{key}</span>')
        html.append(f'        </div>')
        html.append(f'        <div _ngcontent-serverapp-c3289205036="" class="tablecolumn">')
        html.append(f'          <div _ngcontent-serverapp-c3289205036="" class="attribute-value">')
        html.append(f'            <span _ngcontent-serverapp-c3289205036="" class="multiattribute ng-star-inserted">{value}</span>')
        html.append(f'          </div>')
        html.append(f'        </div>')
        html.append(f'      </div>')

    html.append(f'    </div>')
    html.append(f'  </div>')

    # Adding Miscellaneous section
    html.append(f'  <div _ngcontent-serverapp-c3289205036="" class="tablecustom ng-star-inserted">')
    html.append(f'    <div _ngcontent-serverapp-c3289205036="" class="ng-star-inserted">')
    html.append(f'      <p _ngcontent-serverapp-c3289205036="" class="headtable">Miscellaneous</p>')

    for key, value in data["Miscellaneous"].items():
        html.append(f'      <div _ngcontent-serverapp-c3289205036="" class="tablerow ng-star-inserted">')
        html.append(f'        <div _ngcontent-serverapp-c3289205036="" class="tablecolumn">')
        html.append(f'          <span _ngcontent-serverapp-c3289205036="" class="attribute-title">{key}</span>')
        html.append(f'        </div>')
        html.append(f'        <div _ngcontent-serverapp-c3289205036="" class="tablecolumn">')
        html.append(f'          <div _ngcontent-serverapp-c3289205036="" class="attribute-value">')
        html.append(f'            <span _ngcontent-serverapp-c3289205036="" class="multiattribute ng-star-inserted">{value}</span>')
        html.append(f'          </div>')
        html.append(f'        </div>')
        html.append(f'      </div>')

    html.append(f'    </div>')
    html.append(f'  </div>')

    html.append('</div>')

    return '\n'.join(html)

# Generate and print HTML
html_output = generate_html(data)
print(html_output)
