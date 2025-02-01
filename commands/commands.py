from typing import Dict, Any
import logging
from abc import ABC, abstractmethod
from commands.visualization import OSCALVisualizer

class Command(ABC):
    """Base class for all commands"""
    
    @abstractmethod
    def execute(self, oscal_file: Dict[str, Any]) -> None:
        pass
        
    @abstractmethod
    def validate(self, oscal_file: Dict[str, Any]) -> bool:
        pass

class ComponentVisualizerCommand(Command):
    """Command to create visual representation of components"""
    
    def __init__(self):
        self.visualizer = OSCALVisualizer()
    
    def validate(self, oscal_file: Dict[str, Any]) -> bool:
        try:
            return "system-security-plan" in oscal_file and \
                   "system-implementation" in oscal_file["system-security-plan"] and \
                   "components" in oscal_file["system-security-plan"]["system-implementation"]
        except (KeyError, TypeError):
            return False
    
    def execute(self, oscal_file: Dict[str, Any]) -> None:
        try:
            # Generate component graph
            graph_path = self.visualizer.create_component_graph(oscal_file)
            print(f"Component graph generated: {graph_path}")
            
            # Generate HTML report
            report_path = self.visualizer.generate_html_report(oscal_file)
            print(f"HTML report generated: {report_path}")
            
        except Exception as e:
            logging.error(f"Error generating visualizations: {str(e)}")
            print("Failed to create visualizations. Check logs for details.")

class LegacyCommandWrapper(Command):
    """Wrapper to use existing functions in the new command system"""
    
    def __init__(self, legacy_func, validator_func=None):
        self.legacy_func = legacy_func
        self.validator_func = validator_func or (lambda x: True)
    
    def execute(self, oscal_file: Dict[str, Any]) -> None:
        self.legacy_func(oscal_file)
    
    def validate(self, oscal_file: Dict[str, Any]) -> bool:
        return self.validator_func(oscal_file)

class NewRolesCommand(Command):
    """New implementation of the roles command"""
    
    def validate(self, oscal_file: Dict[str, Any]) -> bool:
        return "system-security-plan" in oscal_file and \
               "metadata" in oscal_file["system-security-plan"] and \
               "roles" in oscal_file["system-security-plan"]["metadata"]
    
    def execute(self, oscal_file: Dict[str, Any]) -> None:
        try:
            roles = oscal_file["system-security-plan"]["metadata"]["roles"]
            for role in roles:
                if role["id"] == "owner":
                    print(f"The System Owner is: {role['title']}")
                elif role["id"] == "developer":
                    print(f"The Lead Developer is: {role['title']}")
                elif role["id"] == "system-engineer":
                    print(f"The Lead Engineer is: {role['title']}")
                elif role["id"] == "public-affairs-office":
                    print(f"The Public Affairs Office Lead is: {role['title']}")
        except KeyError as e:
            logging.error(f"Error processing roles: {str(e)}")
            print("No roles found in the SSP.")

class CommandRegistry:
    """Registry that supports both old and new command styles"""
    
    def __init__(self):
        self._commands: Dict[str, Command] = {}
        
    def register(self, name: str, command: Command) -> None:
        self._commands[name] = command
        
    def register_legacy(self, name: str, func, validator=None) -> None:
        """Register an existing function as a command"""
        self._commands[name] = LegacyCommandWrapper(func, validator)
        
    def get_command(self, name: str) -> Command:
        return self._commands.get(name)
        
    def list_commands(self) -> list:
        return list(self._commands.keys())

# Validators for legacy commands
def validate_ssp(oscal_file: Dict[str, Any]) -> bool:
    return "system-security-plan" in oscal_file

def validate_poam(oscal_file: Dict[str, Any]) -> bool:
    return "plan-of-action-and-milestones" in oscal_file

def validate_sap(oscal_file: Dict[str, Any]) -> bool:
    return "assessment-plan" in oscal_file

# Initialize registry with all commands
registry = CommandRegistry()