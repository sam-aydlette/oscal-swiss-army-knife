def list_roles(oscal_ssp):
    roles = oscal_ssp["system-security-plan"]["metadata"]["roles"]
    for role in roles:
        if role["id"] == "owner":
            print (f"The System Owner is:  {role["title"]}")
        else:
            pass
