import xml.etree.ElementTree as ET
from collections import defaultdict
import logging
from pathlib import Path
from typing import Dict, Set, List

def portscheck(scan_file_path: str) -> None:
    """
    Analyze ports and security findings from a Nessus scan file.
    
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

    host_data = defaultdict(lambda: {
        "ports": set(),
        "protocols": set(),
        "os": "",
        "ip": "",
        "findings": defaultdict(list)
    })
    severity_counts = defaultdict(int)
    unique_findings = defaultdict(set)  # Plugin IDs by severity
    fips_findings = []
    eol_findings = []
    
    # Print scan targets from policy preferences
    target_element = root.find('.//preference[name="TARGET"]/value')
    if target_element is not None:
        hostnames = [hostname.strip() for hostname in target_element.text.split(",")]
        print("\nConfigured Scan Targets:")
        for hostname in hostnames:
            print(hostname)

    print("\nScanned Hosts Summary:")
    print("-" * 50)
    
    # Process each host in the results
    for report_host in root.findall(".//ReportHost"):
        hostname = report_host.get("name")
        
        # Get host properties
        props = report_host.find("HostProperties")
        if props is not None:
            for tag in props.findall("tag"):
                if tag.get("name") == "operating-system":
                    host_data[hostname]["os"] = tag.text
                elif tag.get("name") == "host-ip":
                    host_data[hostname]["ip"] = tag.text
        
        # Process findings for this host
        for report_item in report_host.findall("ReportItem"):
            port = report_item.get("port")
            protocol = report_item.get("protocol")
            severity = int(report_item.get("severity", "0"))
            plugin_id = report_item.get("pluginID")
            plugin_name = report_item.get("pluginName", "")
            svc_name = report_item.get("svc_name", "")

            # Process ports (exclude port 0 which is typically used for host-based findings)
            if port != "0":
                host_data[hostname]["ports"].add(port)
                if protocol:
                    host_data[hostname]["protocols"].add(protocol)
                # Store finding details for each port
                host_data[hostname]["findings"][port].append({
                    "service": svc_name,
                    "protocol": protocol,
                    "severity": severity,
                    "name": plugin_name
                })
            
            # Process findings
            if severity > 0:  # Only count actual findings
                severity_counts[severity] += 1
                unique_findings[severity].add(plugin_id)
                
                # Check for FIPS-related findings
                if "FIPS" in plugin_name or "FIPS-140" in plugin_name:
                    fips_findings.append({
                        "host": hostname,
                        "plugin_name": plugin_name,
                        "severity": severity
                    })
                
                # Check for EOL-related findings
                if any(term in plugin_name for term in ["EOL", "End of Life", "end-of-life"]):
                    eol_findings.append({
                        "host": hostname,
                        "plugin_name": plugin_name,
                        "severity": severity
                    })

    # Print detailed host results
    for hostname, data in host_data.items():
        print(f"\nHost: {hostname}")
        if data["ip"]:
            print(f"IP Address: {data['ip']}")
        if data["os"]:
            print(f"Operating System: {data['os']}")
        
        if data["ports"]:
            print("Open Ports:")
            for port in sorted(data["ports"], key=int):
                print(f"  Port {port}/{list(data['protocols'])[0]}:")
                for finding in data["findings"][port]:
                    if finding["service"]:
                        print(f"    Service: {finding['service']}")
                    if finding["severity"] > 0:
                        severity_label = {3: "High", 2: "Medium", 1: "Low"}.get(finding["severity"], "Info")
                        print(f"    Finding: {finding['name']} (Severity: {severity_label})")
        else:
            print("No open ports found in scan results")

    # Print severity statistics
    print("\nFinding Severity Statistics:")
    print("-" * 50)
    severity_labels = {3: "High", 2: "Medium", 1: "Low"}
    for severity in sorted(severity_labels.keys(), reverse=True):
        if severity in severity_counts:
            print(f"{severity_labels[severity]} Severity Findings:")
            print(f"  Total Findings: {severity_counts[severity]}")
            print(f"  Unique Findings: {len(unique_findings[severity])}")

    # Print FIPS-related findings
    if fips_findings:
        print("\nFIPS 140-2 Related Findings:")
        print("-" * 50)
        for finding in fips_findings:
            print(f"Host: {finding['host']}")
            print(f"Finding: {finding['plugin_name']}")
            print(f"Severity: {severity_labels.get(finding['severity'], 'Info')}")
            print()

    # Print EOL-related findings
    if eol_findings:
        print("\nEnd of Life Component Findings:")
        print("-" * 50)
        for finding in eol_findings:
            print(f"Host: {finding['host']}")
            print(f"Finding: {finding['plugin_name']}")
            print(f"Severity: {severity_labels.get(finding['severity'], 'Info')}")
            print()