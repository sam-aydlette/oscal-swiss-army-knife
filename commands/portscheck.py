import xml.etree.ElementTree as ET
from collections import defaultdict

def portscheck(oscal_file):
    #inventory_components = oscal_file["system-security-plan"]["system-implementation"]["inventory-items"]

    # Parse the XML file
    tree = ET.parse("docs/scan_example.xml")
    root = tree.getroot()

    host_data = defaultdict(lambda: {'ports': [], 'protocols': []})

    # Find the list of targeted hosts
    target_element = root.find('.//preference[name="TARGET"]/value')

    if target_element is not None:
        # Split the comma-separated list of hostnames
        hostnames = target_element.text.split(',')
        # Remove any leading/trailing whitespace from each hostname
        hostnames = [hostname.strip() for hostname in hostnames]
        
        print("Scan targets:")
        for hostname in hostnames:
            print(hostname)

        for report_host in root.findall('.//ReportHost'):
            hostname = report_host.get('name')

            for report_item in report_host.findall('ReportItem'):
                port = report_item.get('port')
                protocol = report_item.get('protocol')

                if port != "0":  # Exclude port 0, which is often used for general information
                    if port not in host_data[hostname]['ports']:
                        host_data[hostname]['ports'].append(port)
                    if protocol not in host_data[hostname]['protocols']:
                        host_data[hostname]['protocols'].append(protocol)

        for hostname, data in host_data.items():
            print(f"\nHostname: {hostname}")
            print(f"Ports: {', '.join(sorted(data['ports'], key=int))}")
            print(f"Protocols: {', '.join(sorted(data['protocols']))}")
        
    else:
        print("No open ports found in the scans")
 
