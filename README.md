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


REMINDER:  If you wish to use the poams command, you must use a valid OSCAL POAM file.  For the components and roles command, use an OSCAL SSP file.  For the activities command, use the OSCAL Assessment Plan file.  The file type is distinguished by naming convention.

### To Open The Report
From the terminal, run:

>firefox reports/oscal_report_*.html

### To Create New Commands (Legacy Method) 
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
    registry.register_legacy("mynewcommand", mynewcommand.list_something, validate_ssp)
    
    return registry
```


### To Create New Commands (New Method)
To create new commands using the command handler system, follow these steps:

1. Create your command class in commands/command_handler.py:
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
2. Register your command in the setup_registry() function in main.py:
```python
def setup_registry():
    registry = CommandRegistry()
    # Add your new command
    registry.register("my-new-command", MyNewCommand())
    return registry
```
3. If your command requires utility functions or helper classes:

Add them to commands/utils/ directory
Create a new module (e.g., commands/utils/my_utils.py)
Import and use in your command class


4. For visualization or report generation:

Use the existing OSCALVisualizer class in commands/utils/visualization.py
Reports will be generated in the reports/ directory

Remember to add any new dependencies to requirements.txt if your command needs additional Python packages.

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

![CC BY 4.0][cc-by-shield]

[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
