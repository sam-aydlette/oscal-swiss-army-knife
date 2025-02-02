import argparse
import logging
from typing import Dict, Any, Optional, Callable
from core import core_functionality
from commands import (
    roles, 
    components, 
    poams, 
    activities, 
    portscheck, 
    implemented_controls, 
    security_levels, 
    user_privileges, 
    generate_poam,
    visualize_components,
    monthly_report
)

class CommandRegistry:
    """Registry for command functions with validation"""
    
    def __init__(self):
        self._commands: Dict[str, tuple[Callable, Optional[Callable]]] = {}
        
    def register(self, name: str, func: Callable, validator: Optional[Callable] = None) -> None:
        """Register a command function with optional validator"""
        self._commands[name] = (func, validator)
        
    def get_command(self, name: str) -> Optional[tuple[Callable, Optional[Callable]]]:
        """Get registered command and validator by name"""
        return self._commands.get(name)
        
    def list_commands(self) -> list:
        """List all registered command names"""
        return list(self._commands.keys())

# Validation functions
def validate_ssp(oscal_file: Dict[str, Any]) -> bool:
    """Validate SSP file type"""
    return "system-security-plan" in oscal_file

def validate_poam(oscal_file: Dict[str, Any]) -> bool:
    """Validate POAM file type"""
    return "plan-of-action-and-milestones" in oscal_file

def validate_sap(oscal_file: Dict[str, Any]) -> bool:
    """Validate SAP file type"""
    return "assessment-plan" in oscal_file

def validate_ssp_metadata(oscal_file: Dict[str, Any]) -> bool:
    """Validate SSP metadata exists"""
    return "system-security-plan" in oscal_file and "metadata" in oscal_file["system-security-plan"]

def validate_poam_generator(oscal_file: Dict[str, Any]) -> bool:
    """Validate POAM generator requirements"""
    return validate_poam(oscal_file)

def setup_registry():
    """Set up command registry with commands"""
    registry = CommandRegistry()
    
    registry.register("monthly-report", monthly_report.generate_monthly_report, validate_poam)
    registry.register("visualize-components", visualize_components.visualize_components, validate_ssp)    
    registry.register("roles", roles.list_roles, validate_ssp)
    registry.register("components", components.list_components, validate_ssp)
    registry.register("poams", poams.list_poams, validate_poam)
    registry.register("activities", activities.list_activities, validate_sap)
    registry.register("security-levels", security_levels.analyze_security_levels, validate_ssp_metadata)
    registry.register("user-privileges", user_privileges.analyze_user_privileges, validate_ssp_metadata)
    registry.register("implemented-controls", implemented_controls.analyze_implemented_controls, validate_ssp)
    registry.register("generate-poam", generate_poam.generate_poam, validate_poam_generator)        
    # Register portscheck without OSCAL validation
    registry.register("portscheck", lambda x: portscheck.portscheck(x))
    
    return registry

def execute_command(func: Callable, validator: Optional[Callable], oscal_file: Dict[str, Any], **kwargs) -> None:
    """Execute a command with validation"""
    if validator and not validator(oscal_file):
        print("Command is not valid for this OSCAL file type")
        return
    func(oscal_file, **kwargs)

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
    parser.add_argument("--scan", required=False,
                    help="Path to scan file (required for generate-poam and monthly-report commands)")
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Get command details
        command_result = registry.get_command(args.command)
        if not command_result:
            print(f"Command {args.command} not found")
            return
        
        command_func, validator = command_result
        
        # Handle portscheck command separately
        if args.command == "portscheck":
            command_func(args.file_path)
            return
            
        # Validate scan file argument for commands that require it
        if args.command in ["generate-poam", "monthly-report"] and not args.scan:
            parser.error(f"The {args.command} command requires --scan argument")
        
        # Load the OSCAL file
        oscal_file = core_functionality.load_file(args.file_path)
            
        # Execute command with appropriate arguments
        if args.command == "generate-poam":
            execute_command(command_func, validator, oscal_file, scan_file_path=args.scan)
        elif args.command == "monthly-report":
            command_func(oscal_file, args.scan)
        else:
            execute_command(command_func, validator, oscal_file)
            
    except Exception as e:
        logging.error(f"Error processing command: {str(e)}")
        if args.debug:
            raise
        else:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()