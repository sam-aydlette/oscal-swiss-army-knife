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
    oscal_ssp = core_functionality.load_ssp("docs/ifa_ssp-example.json")

    if hasattr(args, "func"):
        args.func(oscal_ssp)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
