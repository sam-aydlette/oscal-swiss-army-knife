# commands/poam_generator.py
import xml.etree.ElementTree as ET
from datetime import datetime
import uuid
import json
import logging
from typing import Dict, Any, List
from pathlib import Path

def load_existing_poam() -> Dict[str, Any]:
    """Load existing POA&M if available"""
    try:
        poam_path = Path("poam.json")
        if poam_path.exists():
            with poam_path.open('r') as f:
                return json.load(f)
    except Exception as e:
        logging.warning(f"Could not load existing POA&M: {str(e)}")
    
    # Return empty template if no existing POA&M
    return {
        "plan-of-action-and-milestones": {
            "uuid": str(uuid.uuid4()),
            "metadata": {
                "title": "Generated POA&M",
                "last-modified": datetime.now().isoformat(),
                "version": "1.0",
                "oscal-version": "1.1.2"
            },
            "poam-items": []
        }
    }

def ensure_docs_directory() -> Path:
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    return docs_dir

def parse_scan_findings(scan_file_path: str) -> List[Dict[str, Any]]:
    """Parse findings from Nessus scan XML"""
    findings = []
    try:
        tree = ET.parse(scan_file_path)
        root = tree.getroot()
        
        for report_host in root.findall(".//ReportHost"):
            hostname = report_host.get("name")
            
            for report_item in report_host.findall("ReportItem"):
                severity = int(report_item.get("severity", 0))
                # Only process medium and high severity findings
                if severity >= 2:
                    plugin_name = report_item.find("plugin_name")
                    description = report_item.find("description")
                    finding = {
                        "host": hostname,
                        "title": plugin_name.text if plugin_name is not None else "Unknown Finding",
                        "description": description.text if description is not None else "No description available",
                        "severity": severity,
                        "plugin_id": report_item.get("pluginID")
                    }
                    findings.append(finding)
                    
    except Exception as e:
        logging.error(f"Error parsing scan file: {str(e)}")
        raise
        
    return findings

def generate_poam(oscal_file: Dict[str, Any], scan_file_path: str) -> None:
    """
    Generate a POA&M by comparing SSP/POA&M and scan results
    
    Args:
        oscal_file: Loaded OSCAL data (can be SSP or POA&M)
        scan_file_path: Path to Nessus scan XML file
    """
    try:
        # If we got a POA&M file, use it as the existing POA&M
        if "plan-of-action-and-milestones" in oscal_file:
            existing_poam = oscal_file
        else:
            # If we got an SSP, try to load existing POA&M or create new
            existing_poam = load_existing_poam()
            
            # Copy system info from SSP if creating new POA&M
            if "system-security-plan" in oscal_file:
                ssp = oscal_file["system-security-plan"]
                if "metadata" in ssp:
                    existing_poam["plan-of-action-and-milestones"]["metadata"].update({
                        "title": f"POA&M for {ssp['metadata'].get('title', 'Unknown System')}",
                    })
                if "system-characteristics" in ssp and "system-ids" in ssp["system-characteristics"]:
                    existing_poam["plan-of-action-and-milestones"]["system-id"] = ssp["system-characteristics"]["system-ids"][0]

        # Parse scan findings
        scan_findings = parse_scan_findings(scan_file_path)
        
        # Track which existing POA&M items are still valid
        existing_findings = set()
        new_items = []
        
        # Process scan findings
        for finding in scan_findings:
            finding_id = finding["plugin_id"]
            existing_findings.add(finding_id)
            
            # Check if finding already has a POA&M
            has_poam = False
            for item in existing_poam["plan-of-action-and-milestones"].get("poam-items", []):
                if item.get("related-findings", {}).get("plugin_id") == finding_id:
                    has_poam = True
                    # Keep existing POA&M if finding still exists
                    new_items.append(item)
                    break
                    
            if not has_poam:
                # Create new POA&M item for finding
                new_item = {
                    "uuid": str(uuid.uuid4()),
                    "title": finding["title"],
                    "description": finding["description"],
                    "related-findings": {
                        "plugin_id": finding_id,
                        "host": finding["host"],
                        "severity": finding["severity"]
                    }
                }
                new_items.append(new_item)
                
        # Close out POA&M items for resolved findings
        for item in existing_poam["plan-of-action-and-milestones"].get("poam-items", []):
            finding_id = item.get("related-findings", {}).get("plugin_id")
            if finding_id and finding_id not in existing_findings:
                item["status"] = "completed"
                new_items.append(item)
                
        # Update the POA&M with new items
        existing_poam["plan-of-action-and-milestones"]["poam-items"] = new_items
        existing_poam["plan-of-action-and-milestones"]["metadata"]["last-modified"] = datetime.now().isoformat()
       
        # Save the new POA&M
        docs_dir = ensure_docs_directory()
        output_path = docs_dir / f"generated_poam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with output_path.open('w') as f:
            json.dump(existing_poam, f, indent=2)
        print(f"Generated POA&M saved to {output_path}")
            
    except Exception as e:
        logging.error(f"Error generating POA&M: {str(e)}")
        raise