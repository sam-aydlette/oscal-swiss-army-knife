import argparse
import logging
from core import core_functionality
from commands import roles, components, poams, activities, portscheck
from commands.commands import (
    CommandRegistry, 
    NewRolesCommand,
    ComponentVisualizerCommand,
    validate_ssp,
    validate_poam,
    validate_sap
)

def setup_registry():
    """Set up command registry with both old and new commands"""
    registry = CommandRegistry()
    
    # Register the new-style command
    registry.register("new-roles", NewRolesCommand())
    registry.register("visualize-components", ComponentVisualizerCommand())
    
    # Register legacy commands with appropriate validators
    registry.register_legacy("roles", roles.list_roles, validate_ssp)
    registry.register_legacy("components", components.list_components, validate_ssp)
    registry.register_legacy("poams", poams.list_poams, validate_poam)
    registry.register_legacy("activities", activities.list_activities, validate_sap)
    registry.register_legacy("portscheck", portscheck.portscheck, validate_ssp)
    
    return registry

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Set up command registry
    registry = setup_registry()
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="OSCAL Swiss Army Knife")
    parser.add_argument("file_path", help="Path to the JSON file")
    parser.add_argument("command", choices=registry.list_commands(),
                       help="Command to execute")
    parser.add_argument("--debug", action="store_true", 
                       help="Enable debug logging")
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Load the OSCAL file
        oscal_file = core_functionality.load_file(args.file_path)
        
        # Get and execute the command
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