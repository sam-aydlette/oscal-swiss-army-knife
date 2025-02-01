def list_activities(oscal_file):
    assessor_roles = oscal_file["assessment-plan"]["metadata"]["roles"]
    for role in assessor_roles:
        if role.get("id") == "assessor":
            print(f"The 3PAO is: {role.get('title')}")

    activities = oscal_file["assessment-plan"]["local-definitions"]["activities"]
    print()

    for index, activity in enumerate(activities, start=1):
        print(f"Activity #{index}:")
        print(f" Title: {activity['title']}")
        print(f" Description: {activity['steps'][0]['title']}")
        print()
