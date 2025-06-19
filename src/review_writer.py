# src/review_writer.py

import json
import os

def writeReviewReport(filePath: str, flaggedData: list, outputPath="output/review.json"):
    """
    Combines flagged lines and LLM responses into a JSON report.

    Args:
        filePath (str): The input C file reviewed.
        flaggedData (list): List of dictionaries with flagged info and LLM responses.
        outputPath (str): Path to save the final review report.
    """
    report = {
        "file": os.path.basename(filePath),
        "reviews": flaggedData
    }

    os.makedirs(os.path.dirname(outputPath), exist_ok=True)
    
    with open(outputPath, 'w') as outFile:
        json.dump(report, outFile, indent=4)
