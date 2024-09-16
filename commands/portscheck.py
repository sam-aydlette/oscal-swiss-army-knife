import xml.etree.ElementTree as ET

def portscheck(oscal_file):
    #inventory_components = oscal_file["system-security-plan"]["system-implementation"]["inventory-items"]

    # Parse the XML file
    tree = ET.parse("docs/scan_example.xml")
    root = tree.getroot()

    # Find the TARGET preference
    target_element = root.find('.//preference[name="TARGET"]/value')
    
    if target_element is not None:
        # Split the comma-separated list of hostnames
        hostnames = target_element.text.split(',')
        # Remove any leading/trailing whitespace from each hostname
        hostnames = [hostname.strip() for hostname in hostnames]
        print("Hostnames found:")
        for hostname in hostnames:
            print(hostname)
    else:
        print("No open ports found in the scans")
 
