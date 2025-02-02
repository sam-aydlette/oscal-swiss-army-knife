from datetime import datetime
import xml.etree.ElementTree as ET
from typing import Dict, Any, List
from pathlib import Path
import logging
from collections import defaultdict

def calculate_finding_trends() -> List[Dict[str, int]]:
    """Mock function to generate 6-month finding trends"""
    # In a real implementation, this would pull historical data
    return [
        {"month": "Aug", "critical": 10, "high": 20, "medium": 30, "low": 15, "total": 75},
        {"month": "Sep", "critical": 15, "high": 25, "medium": 28, "low": 12, "total": 80},
        {"month": "Oct", "critical": 12, "high": 18, "medium": 32, "low": 14, "total": 76},
        {"month": "Nov", "critical": 8, "high": 22, "medium": 25, "low": 18, "total": 73},
        {"month": "Dec", "critical": 11, "high": 19, "medium": 29, "low": 13, "total": 72},
        {"month": "Jan", "critical": 14, "high": 21, "medium": 27, "low": 16, "total": 78}
    ]

def analyze_scan_findings(scan_file: str) -> Dict[str, Any]:
    """Analyze findings from Nessus scan file"""
    findings = {
        "severity_counts": defaultdict(int),
        "hosts": defaultdict(list),
        "critical_items": []
    }
    
    try:
        tree = ET.parse(scan_file)
        root = tree.getroot()
        
        for host in root.findall(".//ReportHost"):
            hostname = host.get("name")
            
            for item in host.findall("ReportItem"):
                severity = int(item.get("severity", "0"))
                plugin_name = item.get("pluginName", "")
                
                if severity > 0:
                    findings["severity_counts"][severity] += 1
                    findings["hosts"][hostname].append({
                        "severity": severity,
                        "name": plugin_name
                    })
                    
                    if severity >= 3:
                        findings["critical_items"].append({
                            "host": hostname,
                            "finding": plugin_name
                        })
                        
    except Exception as e:
        logging.error(f"Error analyzing scan file: {str(e)}")
        
    return findings

def analyze_poams(poam_file: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze POA&M items"""
    poam_data = {
        "open_items": [],
        "recently_closed": [],
        "approaching_deadline": []
    }
    
    try:
        if "plan-of-action-and-milestones" in poam_file:
            poam_items = poam_file["plan-of-action-and-milestones"].get("poam-items", [])
            
            for item in poam_items:
                title = item.get("title", "")
                status = item.get("status", "open")
                
                if status == "open":
                    poam_data["open_items"].append(title)
                elif status == "completed":
                    poam_data["recently_closed"].append(title)
                    
    except Exception as e:
        logging.error(f"Error analyzing POA&Ms: {str(e)}")
        
    return poam_data

def generate_monthly_report(oscal_file: Dict[str, Any], scan_file_path: str) -> None:
    """Generate monthly security report combining scan and POA&M data"""
    try:
        # Get template
        template_path = Path("docs/monthly-report-template.md")
        if not template_path.exists():
            raise FileNotFoundError("Report template not found")
            
        template_content = template_path.read_text()
        
        # Get system name from SSP or POA&M
        system_name = "Unknown System"
        system_id = "Unknown ID"
        
        if "system-security-plan" in oscal_file:
            metadata = oscal_file["system-security-plan"].get("metadata", {})
            system_name = metadata.get("title", system_name)
        elif "plan-of-action-and-milestones" in oscal_file:
            metadata = oscal_file["plan-of-action-and-milestones"].get("metadata", {})
            system_name = metadata.get("title", system_name)
            
        # Analyze current findings
        scan_findings = analyze_scan_findings(scan_file_path)
        poam_data = analyze_poams(oscal_file)
        
        # Get historical trends
        trends = calculate_finding_trends()
        
        # Generate report content
        report_content = template_content.replace("System Name and ID", f"{system_name} ({system_id})")
        
        # Add finding statistics
        stats_text = "\n### Current Finding Statistics\n\n"
        severity_labels = {4: "Critical", 3: "High", 2: "Medium", 1: "Low"}
        for severity, label in severity_labels.items():
            count = scan_findings["severity_counts"][severity]
            stats_text += f"- {label}: {count} findings\n"
            
        report_content = report_content.replace("System overview and key information goes here.", 
            f"System overview and key information goes here.\n{stats_text}")
            
        # Add POA&M information
        poam_text = "\n### POA&M Status\n\n"
        poam_text += f"- Open Items: {len(poam_data['open_items'])}\n"
        poam_text += f"- Recently Closed: {len(poam_data['recently_closed'])}\n"
        
        report_content = report_content.replace("**High Priority:**",
            f"{poam_text}\n**High Priority:**")
            
        # Update timestamp
        now = datetime.now()
        report_content = report_content.replace("January 31, 2025", 
            now.strftime("%B %d, %Y"))
            
        # Save report
        output_path = Path("reports") / f"monthly_report_{now.strftime('%Y%m')}.md"
        output_path.parent.mkdir(exist_ok=True)
        output_path.write_text(report_content)
        
        print(f"Monthly report generated: {output_path}")
        
    except Exception as e:
        logging.error(f"Error generating monthly report: {str(e)}")
        raise