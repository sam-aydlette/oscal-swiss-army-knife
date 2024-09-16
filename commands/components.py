def list_components(oscal_file):
    components = oscal_file["system-security-plan"]["system-implementation"]["inventory-items"]
    for component in components:
        print(f"Description: {component['description']}")

        print("Properties:")
        for prop in component["props"]:
            name = prop["name"]
            value = prop["value"]
            prop_class = prop.get("class", "")
            print(f"  {name}: {value} ({prop_class})")

        print("Implemented Components:")
        implemented_components = component.get("implemented-components", [])
        for imp_comp in implemented_components:
            component_props = imp_comp.get("props", [])
            for comp_prop in component_props:
                name = comp_prop["name"]
                value = comp_prop["value"]
                print(f"    {name}: {value}")

        print()