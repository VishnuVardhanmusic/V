# src/code_parser.py

import re

def parseCodeForViolations(filePath: str):
    """
    Parses the C/C++ file and flags lines that potentially violate known guidelines.

    Args:
        filePath (str): Path to the .c or .h file

    Returns:
        List[dict]: List of flagged lines with metadata
    """
    flaggedLines = []
    currentFunction = None
    lineCountInFunction = 0
    insideFunction = False

    with open(filePath, 'r') as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        stripped = line.strip()

        # Track functions for rule G005
        if re.match(r'\w+\s+\w+\(.*\)\s*{', stripped):
            insideFunction = True
            currentFunction = stripped
            lineCountInFunction = 1
        elif insideFunction:
            if "}" in stripped:
                insideFunction = False
                if lineCountInFunction > 50:
                    flaggedLines.append({
                        "line": idx + 1,
                        "code": stripped,
                        "guideline_id": "G005",
                        "reason": "Function exceeds 50 lines"
                    })
            else:
                lineCountInFunction += 1

        # Rule G001: printf inside ISR
        if "ISR" in stripped and "{" in stripped:
            for offset in range(1, 10):  # Check next few lines for printf
                if idx + offset < len(lines) and "printf" in lines[idx + offset]:
                    flaggedLines.append({
                        "line": idx + offset + 1,
                        "code": lines[idx + offset].strip(),
                        "guideline_id": "G001",
                        "reason": "Use of printf inside ISR"
                    })
                    break

        # Rule G002: goto
        if "goto" in stripped:
            flaggedLines.append({
                "line": idx + 1,
                "code": stripped,
                "guideline_id": "G002",
                "reason": "Usage of goto"
            })

        # Rule G003: uninitialized local variable
        if re.match(r"int\s+\w+\s*;", stripped):  # crude check
            flaggedLines.append({
                "line": idx + 1,
                "code": stripped,
                "guideline_id": "G003",
                "reason": "Possibly uninitialized local variable"
            })

        # Rule G004: magic number (e.g., hardcoded values > 10)
        if re.search(r"\b\d{2,}\b", stripped) and not re.search(r"#define|const", stripped):
            flaggedLines.append({
                "line": idx + 1,
                "code": stripped,
                "guideline_id": "G004",
                "reason": "Magic number detected"
            })

    return flaggedLines
