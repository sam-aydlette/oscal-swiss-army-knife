# oscal-cli
a CLI tool that allows users to manipulate OSCAL formatted data by running commands in the terminal.

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
To use the OSCAL CLI, run:

>python main.py [docs/oscal_file.json] [command]  

Valid commands:  
>roles    

The roles command lists the roles and responsibilities for the system.   

>components  

The components command lists the inventory components for the system.   

>poams  

The poams command lists the open POA&M items for the system.    

>activities  

The activities command lists the activities performed in the Security Assessment by the 3PAO.  


REMINDER:  If you wish to use the poams command, you must use a valid OSCAL POAM file.  For the components and roles command, use an OSCAL SSP file.  For the activities command, use the OSCAL Assessment Plan file.  The file type is distinguished by naming convention.
