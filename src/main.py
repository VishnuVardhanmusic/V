# src/main.py

import sys
from guidelines_loader import loadGuidelines
from code_parser import parseCodeForViolations
from review_agent import getReviewFromLLM
from review_writer import writeReviewReport

def main(inputFilePath):
    print(f"🔍 Reviewing file: {inputFilePath}")
    
    # Step 1: Load Guidelines
    guidelines = loadGuidelines("guidelines/c_guidelines.json")
    
    # Step 2: Parse code and flag potential violations
    flaggedLines = parseCodeForViolations(inputFilePath)
    
    # Step 3: Enrich each flagged line with LLM review
    enrichedReviews = []
    for item in flaggedLines:
        guidelineId = item["guideline_id"]
        codeLine = item["code"]
        description = guidelines.get(guidelineId, "No description found")
        
        print(f"📌 Checking line {item['line']} for {guidelineId}...")
        llmReview = getReviewFromLLM(codeLine, description)
        
        enrichedReviews.append({
            "line": item["line"],
            "code": codeLine,
            "guideline_id": guidelineId,
            "description": description,
            "is_violation": llmReview.get("is_violation"),
            "reasoning": llmReview.get("reasoning"),
            "suggestion": llmReview.get("suggestion")
        })
    
    # Step 4: Save final review output
    writeReviewReport(inputFilePath, enrichedReviews)
    print("✅ Review complete. Output saved to output/review.json")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Usage: python src/main.py test_cases/c_code.c")
    else:
        main(sys.argv[1])
