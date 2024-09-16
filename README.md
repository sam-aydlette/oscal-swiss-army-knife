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

### To Create New Commands 
To create new commands in the OSCAL Swiss Army Knife CLI, you must update the following files:
- In "main.py" update the main function with a new command argument and import the command
- In /commands directory create a new .py file with the script you want to execute
- Place any documents in the docs folder that are required for the command to run


