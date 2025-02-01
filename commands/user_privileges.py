def analyze_user_privileges(oscal_file):
    """Analyzes and reports on user privileges and roles in the system"""
    users = oscal_file["system-security-plan"]["system-implementation"]["users"]
    roles = {role["id"]: role["title"] 
            for role in oscal_file["system-security-plan"]["metadata"]["roles"]}
    
    print("\nUser Privilege Analysis")
    print("=====================")
    
    for user in users:
        print(f"\nUser: {user.get('title', 'Unnamed')}")
        
        # Print user type if specified
        user_type = next((prop["value"] for prop in user.get("props", []) 
                        if prop["name"] == "type"), "Not specified")
        print(f"Type: {user_type}")
        
        # Print assigned roles
        print("Assigned Roles:")
        for role_id in user.get("role-ids", []):
            print(f"- {roles.get(role_id, role_id)}")
        
        # Print authorized privileges
        if "authorized-privileges" in user:
            print("Authorized Privileges:")
            for privilege in user["authorized-privileges"]:
                print(f"- {privilege.get('title', 'Unnamed privilege')}:")
                for function in privilege.get("functions-performed", []):
                    print(f"  * {function}")