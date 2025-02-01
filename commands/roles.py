def list_roles(oscal_file):
    roles = oscal_file["system-security-plan"]["metadata"]["roles"]
    for role in roles:
        if role["id"] == "owner":
            print(f"The System Owner is:  {role['title']}")
        elif role["id"] == "developer":
            print(f"The Lead Developer is: {role['title']}")
        elif role["id"] == "system-engineer":
            print(f"The Lead Engineer is: {role['title']}")
        elif role["id"] == "public-affairs-office":
            print(f"The Public Affairs Office Lead is: {role['title']}")
        else:
            print("No roles found in the SSP.")
