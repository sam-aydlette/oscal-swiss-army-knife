def analyze_security_levels(oscal_file):
    """Analyzes and reports on the security impact levels across the system"""
    characteristics = oscal_file["system-security-plan"]["system-characteristics"]
    impact_levels = characteristics["security-impact-level"]
    
    print("\nSecurity Impact Level Analysis")
    print("=============================")
    print(f"Confidentiality: {impact_levels.get('security-objective-confidentiality', 'Not specified')}")
    print(f"Integrity: {impact_levels.get('security-objective-integrity', 'Not specified')}")
    print(f"Availability: {impact_levels.get('security-objective-availability', 'Not specified')}")
    
    # Analyze information types if present
    if "system-information" in characteristics:
        print("\nInformation Type Details:")
        for info_type in characteristics["system-information"].get("information-types", []):
            print(f"\nTitle: {info_type.get('title', 'Unnamed')}")
            print(f"Description: {info_type.get('description', 'No description')}")
            
            impacts = {
                "Confidentiality": info_type.get("confidentiality-impact", {}),
                "Integrity": info_type.get("integrity-impact", {}),
                "Availability": info_type.get("availability-impact", {})
            }
            
            for impact_type, impact_data in impacts.items():
                base = impact_data.get("base", "Not specified")
                selected = impact_data.get("selected", "Same as base")
                if "adjustment-justification" in impact_data:
                    print(f"{impact_type}: {base} (Adjusted to {selected})")
                    print(f"Justification: {impact_data['adjustment-justification']}")
                else:
                    print(f"{impact_type}: {base}")