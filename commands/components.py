def list_components(oscal_ssp):
    components = oscal_ssp["system-security-plan"]["system-implementation"]["inventory-items"]
    for component in components:

        print(f"Component: {component["implemented-components"]}")
        print("\n")
