import argparse
from commands import roles
from core import core_functionality

def main():
    parser = argparse.ArgumentParser(description="My CLI Tool")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Add the 'roles' command
    roles_parser = subparsers.add_parser("roles", help="List the roles from the SSP")
    roles_parser.set_defaults(func=roles.list_roles)

    args = parser.parse_args()

    # Load the OSCAL SSP dictionary

    # Prompt the user for the file path
    file_path = input("Enter the path to the JSON file: ")

    # Load the OSCAL SSP dictionary
    try:
        oscal_ssp = core_functionality.load_ssp(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return
    if hasattr(args, "func"):
        args.func(oscal_ssp)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
