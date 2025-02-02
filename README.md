# OSCAL Swiss Army Knife

A command-line interface (CLI) tool for analyzing and manipulating OSCAL (Open Security Controls Assessment Language) formatted data along with associated machine-generated security data.

## Prerequisites

- Python 3.x
- Git

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Unix/macOS
env\Scripts\activate     # On Windows
```

2. Clone the repository:
```bash
git clone https://github.com/path/to/repo
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic command syntax:
```bash
python main.py <oscal_file> <command> [options]
```

### Available Commands

| Command | Description | Required File Type |
|---------|-------------|-------------------|
| `roles` | Lists system roles and responsibilities | SSP |
| `components` | Lists system inventory components | SSP |
| `poams` | Lists open Plan of Action & Milestones items | POA&M |
| `activities` | Lists 3PAO assessment activities | SAP |
| `security-levels` | Analyzes security impact levels and information types | SSP |
| `user-privileges` | Lists user roles and authorized privileges | SSP |
| `implemented-controls` | Analyzes security control implementations | SSP |
| `portscheck` | Analyzes open ports and findings from scan results | Scan |
| `visualize-components` | Generates component visualization report | SSP |
| `generate-poam` | Creates POA&M from scan findings | POA&M/Scan |
| `monthly-report` | Generates a monthly report in markdown | POA&M/Scan |

### Options

- `--debug`: Enable debug logging
- `--scan <file>`: Path to scan file (required for generate-poam and monthly-report command)

### Examples

List system roles:
```bash
python main.py system_security_plan.json roles
```

Generate POA&M from scan:
```bash
python main.py existing_poam.json generate-poam --scan scan_results.xml
```

### Viewing Reports

To view generated reports:
```bash
firefox reports/oscal_report_*.html
```

## Development Guide

### Creating New Commands

1. Create a new .py file in the `/commands` directory with your command function:
```python
# commands/mynewcommand.py
def list_something(oscal_file):
    # Your command logic here
    print("Command output...")
```

2. Update `main.py` to include your command:
```python
def setup_registry():
    registry = CommandRegistry()
    
    # Add your new command with appropriate validator
    registry.register("mynewcommand", mynewcommand.list_something, validate_ssp)
    
    return registry
```

**Note:** Remember to add any new dependencies to `requirements.txt` if your command needs additional Python packages.

## License

Licensed under [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

![CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)