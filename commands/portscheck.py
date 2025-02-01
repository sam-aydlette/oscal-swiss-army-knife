import xml.etree.ElementTree as ET
from collections import defaultdict
import logging
from pathlib import Path

def portscheck(scan_file_path: str) -> None:
    """
    Analyze ports from a Nessus scan file.
    
    Args:
        scan_file_path: Path to the Nessus scan XML file
    """
    try:
        # Parse the XML file
        tree = ET.parse(scan_file_path)
        root = tree.getroot()
    except FileNotFoundError:
        print(f"Error: Scan file not found: {scan_file_path}")
        return
    except ET.ParseError as e:
        print(f"Error: Failed to parse scan file: {str(e)}")
        return
    except Exception as e:
        print(f"Error processing scan file: {str(e)}")
        return

    host_data = defaultdict(lambda: {"ports": [], "protocols": []})

    # Find the list of targeted hosts
    target_element = root.find('.//preference[name="TARGET"]/value')

    if target_element is not None:
        # Split the comma-separated list of hostnames
        hostnames = [hostname.strip() for hostname in target_element.text.split(",")]
        
        print("\nScan targets:")
        for hostname in hostnames:
            print(hostname)

        for report_host in root.findall(".//ReportHost"):
            hostname = report_host.get("name")
            
            # Process ports
            for report_item in report_host.findall("ReportItem"):
                port = report_item.get("port")
                protocol = report_item.get("protocol")

                if port != "0":  # Exclude port 0
                    if port not in host_data[hostname]["ports"]:
                        host_data[hostname]["ports"].append(port)
                    if protocol not in host_data[hostname]["protocols"]:
                        host_data[hostname]["protocols"].append(protocol)

        # Print results
        print("\nPort Scan Results:")
        print("-" * 50)
        for hostname, data in host_data.items():
            print(f"\nHostname: {hostname}")
            print(f"Ports: {', '.join(sorted(data['ports'], key=int))}")
            print(f"Protocols: {', '.join(sorted(data['protocols']))}")

    else:
        print("No scan targets found in the XML file")
