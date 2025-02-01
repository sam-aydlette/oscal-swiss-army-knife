import json
from typing import Dict, Any, Optional
import logging
from pathlib import Path

class OSCALError(Exception):
    """Base exception class for OSCAL-related errors"""
    pass

class FileFormatError(OSCALError):
    """Raised when file format is invalid"""
    pass

class ValidationError(OSCALError):
    """Raised when OSCAL validation fails"""
    pass

def setup_logging(log_level: str = 'INFO') -> None:
    """Configure logging for the application"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def validate_oscal_type(data: Dict[str, Any]) -> str:
    """
    Determine the type of OSCAL document
    
    Returns:
        str: One of 'ssp', 'poam', 'sap', or 'unknown'
    """
    if "system-security-plan" in data:
        return "ssp"
    elif "plan-of-action-and-milestones" in data:
        return "poam"
    elif "assessment-plan" in data:
        return "sap"
    return "unknown"

def load_file(file_path: str) -> Dict[str, Any]:
    """
    Load and validate an OSCAL JSON file
    
    Args:
        file_path: Path to the OSCAL JSON file
        
    Returns:
        Dict containing the parsed OSCAL data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        FileFormatError: If file is not valid JSON
        ValidationError: If content is not valid OSCAL
    """
    try:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with path.open('r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                raise FileFormatError(f"Invalid JSON format: {str(e)}")
                
        # Validate it's an OSCAL document
        doc_type = validate_oscal_type(data)
        if doc_type == "unknown":
            raise ValidationError("File does not appear to be a valid OSCAL document")
            
        logging.info(f"Successfully loaded OSCAL {doc_type.upper()} from {file_path}")
        return data
        
    except Exception as e:
        logging.error(f"Error loading file {file_path}: {str(e)}")
        raise

def get_metadata(oscal_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract metadata from any OSCAL document type"""
    doc_type = validate_oscal_type(oscal_data)
    
    if doc_type == "unknown":
        return None
        
    try:
        if doc_type == "ssp":
            return oscal_data["system-security-plan"]["metadata"]
        elif doc_type == "poam":
            return oscal_data["plan-of-action-and-milestones"]["metadata"]
        elif doc_type == "sap":
            return oscal_data["assessment-plan"]["metadata"]
    except KeyError:
        logging.warning("Metadata section not found in document")
        return None