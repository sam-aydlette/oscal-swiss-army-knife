def analyze_implemented_controls(oscal_file):
    """Lists and analyzes implemented security controls"""
    implementation = oscal_file["system-security-plan"]["control-implementation"]
    
    print("\nImplemented Controls Analysis")
    print("==========================")
    print(f"Description: {implementation.get('description', 'No description provided')}")
    
    for req in implementation.get("implemented-requirements", []):
        print(f"\nControl ID: {req.get('control-id', 'Unknown')}")
        
        # Print statements if present
        if "statements" in req:
            print("Statements:")
            for stmt in req["statements"]:
                print(f"- ID: {stmt.get('statement-id', 'Unknown')}")
                
                # Print component implementations
                if "by-components" in stmt:
                    print("  Implemented By Components:")
                    for comp in stmt["by-components"]:
                        print(f"  * Component: {comp.get('component-uuid', 'Unknown')}")
                        print(f"    Description: {comp.get('description', 'No description')}")
                        
                        # Print parameters if set
                        if "set-parameters" in comp:
                            print("    Parameters:")
                            for param in comp["set-parameters"]:
                                print(f"    - {param['param-id']}: {', '.join(param['values'])}")