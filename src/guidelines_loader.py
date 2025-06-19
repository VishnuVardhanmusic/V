# src/guideline_loader.py

import json
import os

def loadGuidelines(filePath: str):
    """
    Load coding guidelines from the given JSON file.
    
    Args:
        filePath (str): Path to the JSON file containing guidelines.
    
    Returns:
        dict: Dictionary mapping guideline ID to description.
    """
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"Guidelines file not found: {filePath}")
    
    with open(filePath, 'r') as file:
        guidelines = json.load(file)
    
    return {rule['id']: rule['description'] for rule in guidelines}
