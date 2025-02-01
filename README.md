# oscal-swiss-army-knife
a CLI tool that allows users to manipulate OSCAL formatted data by running commands in the terminal.  This is the Swiss Army Knife of OSCAL tools!

### Prerequisites  
Python 3  
Git  

To use the tool, first set up your local environment:

>pip install virtualenv  
>source env/bin/activate  
>pip install -r requirements.txt  

Then, clone the repository to your working directory:
> git clone https : // github/path/to/repo


### Instructions  
To use the OSCAL Swiss Army Knife CLI, run:

>python main.py [docs/oscal_file.json] [command]  

Valid commands:  
>roles

The roles command lists the roles and responsibilities for the system.  It is derived from the SSP.   

>components

The components command lists the Inventory components for the system.  It is derived from the SSP

>poams

The poams command lists the open POA&M items for the system.  It is derived from the POA&M  

>activities

The activities command lists the activities to be performed by the 3PAO.  It is derived from the SAP.  

>security-levels

The security-levels command analyzes and displays the security impact levels and information types defined in the SSP.

>user-privileges

The user-privileges command lists all users, their roles, and authorized privileges as defined in the SSP.

>implemented-controls

The implemented-controls command analyzes and displays details about security control implementations defined in the SSP.

>portscheck

The portscheck commmand lists all components targeted in the scan, open ports, and findings. It uses the scan xml file.

>visualize-components

The visualize-components command generates a report and graphic representing the OSCAL data.

>generate-poam

The generate-poam command generates a POA&M, deriving entries from previous POA&Ms that remain open and new scan findings. It requires an argument --scan


REMINDER:  If you wish to use the poams command, you must use a valid OSCAL POAM file.  For the components and roles command, use an OSCAL SSP file.  For the activities command, use the OSCAL Assessment Plan file.  The file type is distinguished by naming convention.

### To Open The Report
From the terminal, run:

>firefox reports/oscal_report_*.html

### To Create New Commands
1. Create a new .py file in the /commands directory with your command function:
```python
# commands/mynewcommand.py
def list_something(oscal_file):
    # Your command logic here
    print("Command output...")
```
2. Update main.py to include your command:
```python
def setup_registry():
    registry = CommandRegistry()
    
    # Add your new command with appropriate validator
    registry.register("mynewcommand", mynewcommand.list_something, validate_ssp)
    
    return registry
```

2. Create your command class in commands/commands.py:
   - Inherit from the Command base class
   - Implement the validate() method to check if the command can run with the given OSCAL file
   - Implement the execute() method with your command's functionality
   
Example:
```python
class MyNewCommand(Command):
    def validate(self, oscal_file: Dict[str, Any]) -> bool:
        return "required-section" in oscal_file
        
    def execute(self, oscal_file: Dict[str, Any]) -> None:
        # Your command logic here
        print("Executing new command...")
```

Remember to add any new dependencies to requirements.txt if your command needs additional Python packages.

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

![CC BY 4.0][cc-by-shield]

[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
