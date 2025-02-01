def list_poams(oscal_file):
    poams = oscal_file["plan-of-action-and-milestones"]["poam-items"]
    print(f"Total number of POAM items: {len(poams)}")
    print()

    for index, poam in enumerate(poams, start=1):
        print(f"POAM Item {index}:")
        print(f"  Title: {poam['title']}")
        print(f"  Description: {poam['description']}")

        print()
