import argparse
import logging
from core import core_functionality
from commands import roles, components, poams, activities, portscheck, implemented_controls, security_levels, user_privileges
from commands.commands import (
    CommandRegistry, 
    NewRolesCommand,
    ComponentVisualizerCommand,
    validate_ssp,
    validate_poam,
    validate_sap,
    validate_ssp_metadata
)

def setup_registry():
    """Set up command registry with both old and new commands"""
    registry = CommandRegistry()
    
    # Register the new-style commands
    registry.register("new-roles", NewRolesCommand())
    registry.register("visualize-components", ComponentVisualizerCommand())
    
    # Register legacy commands with appropriate validators
    registry.register_legacy("roles", roles.list_roles, validate_ssp)
    registry.register_legacy("components", components.list_components, validate_ssp)
    registry.register_legacy("poams", poams.list_poams, validate_poam)
    registry.register_legacy("activities", activities.list_activities, validate_sap)
    registry.register_legacy("security-levels", security_levels.analyze_security_levels, validate_ssp_metadata)
    registry.register_legacy("user-privileges", user_privileges.analyze_user_privileges, validate_ssp_metadata)
    registry.register_legacy("implemented-controls", implemented_controls.analyze_implemented_controls, validate_ssp)
    
    # Register portscheck without OSCAL validation
    registry.register_legacy("portscheck", lambda x: portscheck.portscheck(x))
    
    return registry

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Set up command registry
    registry = setup_registry()
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="OSCAL Swiss Army Knife")
    parser.add_argument("file_path", help="Path to the input file (OSCAL JSON or scan XML)")
    parser.add_argument("command", choices=registry.list_commands(),
                       help="Command to execute")
    parser.add_argument("--debug", action="store_true", 
                       help="Enable debug logging")
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        if args.command == "portscheck":
            # For portscheck, pass the file path directly
            command = registry.get_command("portscheck")
            command.execute(args.file_path)
        else:
            # For OSCAL commands, load and validate the file
            oscal_file = core_functionality.load_file(args.file_path)
            command = registry.get_command(args.command)
            if command and command.validate(oscal_file):
                command.execute(oscal_file)
            else:
                print(f"Command {args.command} is not valid for this OSCAL file type")
            
    except Exception as e:
        logging.error(f"Error processing command: {str(e)}")
        if args.debug:
            raise
        else:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()