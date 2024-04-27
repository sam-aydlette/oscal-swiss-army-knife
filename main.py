import argparse
from commands import roles, components, poams, activities
from core import core_functionality

def main():
    parser = argparse.ArgumentParser(description="My CLI Tool")
    parser.add_argument("file_path", help="Path to the JSON file")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Add the 'roles' command
    roles_parser = subparsers.add_parser("roles", help="List the roles from the SSP")
    roles_parser.set_defaults(func=roles.list_roles)

    # Add the 'components' command
    components_parser = subparsers.add_parser("components", help="List the components from the SSP")
    components_parser.set_defaults(func=components.list_components)

    # Add the 'poams' command
    poams_parser = subparsers.add_parser("poams", help="List the POAM items from the JSON file")
    poams_parser.set_defaults(func=poams.list_poams)

    # Add the 'activities' command
    activities_parser = subparsers.add_parser("activities", help="List the Assessor Activity items from the JSON file")
    activities_parser.set_defaults(func=activities.list_activities)


    args = parser.parse_args()

    # Load the OSCAL SSP dictionary
    try:
        oscal_ssp = core_functionality.load_ssp(args.file_path)
    except FileNotFoundError:
        print(f"File not found: {args.file_path}")
        return

    if hasattr(args, "func"):
        args.func(oscal_ssp)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()