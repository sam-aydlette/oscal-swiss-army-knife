# oscal-cli
a CLI tool that allows users to manipulate OSCAL formatted data by running commands in the terminal.

### Prerequisites  
Python 3
Git 

To use the tool, first set up your local environment:

>pip install virtualenv
>source env/bin/activate
>pip install -r requirements.txt

Clone the repository to a directory:
>git clone https://path-to-github-repo


### Instructions  
To use the OSCAL CLI, run:

python main.py [path/to/oscal_file] [command]

Valid commands:  
-roles  
-components  
-poams  
-activities  

REMINDER:  If you wish to use the poams command, you must use a valid OSCAL POAM file.  For the components and roles command, use an OSCAL SSP file.  For the activities command, use the OSCAL Assessment Plan file.  The file type is distinguished by naming convention.
