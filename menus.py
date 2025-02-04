# menus.py
from typing import Dict, List, TypedDict
from dataclasses import dataclass

class MenuItem(TypedDict):
    name: str
    description: str
    url: str
    keywords: List[str]
    context: str

# Query enhancers for semantic understanding
QUERY_ENHANCERS: Dict[str, str] = {
    "check": "evaluation verification assessment",
    "marks": "score points grade evaluation",
    "report": "details information data",
    "exam": "examination test assessment",
    "digital": "online electronic computer-based",
    "question": "answer problem solution",
    "failed": "supplementary repeat retake",
    "grace": "additional extra bonus",
    "revaluation": "recheck review reassess",
    "modify": "change update alter",
    "result": "outcome score performance",
    "paper": "answer sheet exam script",
}

MENUS: List[MenuItem] = [
    {
        "name": "Revaluation Report",
        "description": "Revaluation EVALUATION_REPORT",
        "url": "revaluation-report",
        "keywords": [
            "recheck marks", "review evaluation", "reassessment",
            "check marks again", "second evaluation", "mark verification",
            "change in marks", "correction in evaluation"
        ],
        "context": "Used when students want their answer sheets to be evaluated again"
    },
    {
        "name": "Grace Mark Report",
        "description": "Grace Mark Report",
        "url": "grace-mark-report",
        "keywords": [
            "additional marks", "bonus points", "extra marks",
            "mark addition", "special consideration", "passing grace",
            "sports grace", "cultural grace", "medical grace"
        ],
        "context": "For viewing and managing additional marks given to students under various policies"
    },
    {
        "name": "Supplementary Report",
        "description": "Supplementary Report",
        "url": "supplementary-report",
        "keywords": [
            "supply exam", "repeat exam", "failed subjects",
            "pending papers", "clearing backlogs", "additional attempt",
            "improvement exam"
        ],
        "context": "Report for students who need to retake exams or clear pending subjects"
    },
    {
        "name": "Moderation Report",
        "description": "Moderation Report",
        "url": "moderation-report",
        "keywords": [
            "mark adjustment", "score normalization", "standardization",
            "scaling of marks", "mark modification", "result moderation",
            "batch correction"
        ],
        "context": "Used for reviewing and adjusting marks across different evaluators or centers"
    },
    {
        "name": "Exam Valuation Report",
        "description": "Exam Valuation Report (Regular)",
        "url": "exam-valuation-report",
        "keywords": [
            "regular evaluation", "main exam marks", "first evaluation",
            "primary assessment", "semester evaluation", "term end marks",
            "final marks"
        ],
        "context": "Primary report for regular examination evaluation results"
    },
    {
        "name": "Digital Valuation Report",
        "description": "Digital Valuation Report",
        "url": "digital-valuation-report",
        "keywords": [
            "online evaluation", "digital marking", "e-evaluation",
            "computer based assessment", "electronic marking",
            "screen evaluation", "digital scoring"
        ],
        "context": "Report for exams that were evaluated digitally or through online platforms"
    },
    {
        "name": "Student Question Wise Mark Report",
        "description": "Student Question Wise Mark Report",
        "url": "student-question-wise-mark-report",
        "keywords": [
            "question analysis", "per question marks", "detailed marks",
            "question-by-question", "answer analysis", "mark distribution",
            "question pattern performance"
        ],
        "context": "Detailed analysis of marks obtained in each question by students"
    },
    {
        "name": "Student Performance Report",
        "description": "Comprehensive Student Performance Report",
        "url": "student-performance-report",
        "keywords": [
            "overall performance", "academic progress", "semester wise marks",
            "cumulative score", "grade history", "academic history",
            "student assessment", "performance analysis"
        ],
        "context": "Complete overview of a student's academic performance across all evaluations"
    },
    {
        "name": "Attendance Report",
        "description": "Student Attendance Report",
        "url": "attendance-report",
        "keywords": [
            "attendance record", "class presence", "absence record",
            "attendance percentage", "participation record", "attendance shortage",
            "attendance eligibility"
        ],
        "context": "Report showing student's attendance records and eligibility status"
    },
    {
        "name": "Internal Assessment Report",
        "description": "Internal Assessment Mark Report",
        "url": "internal-assessment-report",
        "keywords": [
            "internal marks", "continuous assessment", "class test marks",
            "assignment scores", "project evaluation", "practical marks",
            "internal evaluation"
        ],
        "context": "Report for internal assessment marks including assignments, projects, and class tests"
    },
    {
        "name": "Consolidated Mark Report",
        "description": "Consolidated Mark Sheet",
        "url": "consolidated-mark-report",
        "keywords": [
            "final marksheet", "complete marks", "consolidated score",
            "overall marks", "total assessment", "final evaluation",
            "complete academic record"
        ],
        "context": "Comprehensive report combining all evaluations and assessments"
    },
    {
        "name": "Semester Result Report",
        "description": "Semester-wise Result Report",
        "url": "semester-result-report",
        "keywords": [
            "semester results", "term end results", "semester grades",
            "period assessment", "term evaluation", "semester performance",
            "term wise marks"
        ],
        "context": "Results and performance analysis for specific academic terms or semesters"
    }
]

# Validation function to ensure all menu items follow the required structure
def validate_menu_items() -> None:
    """
    Validates that all menu items have the required fields and proper data types.
    Raises ValueError if validation fails.
    """
    required_fields = {'name', 'description', 'url', 'keywords', 'context'}
    
    for idx, item in enumerate(MENUS):
        # Check if all required fields are present
        if not all(field in item for field in required_fields):
            missing_fields = required_fields - set(item.keys())
            raise ValueError(f"Menu item at index {idx} is missing required fields: {missing_fields}")
        
        # Check data types
        if not isinstance(item['name'], str):
            raise ValueError(f"Menu item at index {idx}: 'name' must be a string")
        if not isinstance(item['description'], str):
            raise ValueError(f"Menu item at index {idx}: 'description' must be a string")
        if not isinstance(item['url'], str):
            raise ValueError(f"Menu item at index {idx}: 'url' must be a string")
        if not isinstance(item['keywords'], list):
            raise ValueError(f"Menu item at index {idx}: 'keywords' must be a list")
        if not isinstance(item['context'], str):
            raise ValueError(f"Menu item at index {idx}: 'context' must be a string")
        
        # Check that all keywords are strings
        if not all(isinstance(k, str) for k in item['keywords']):
            raise ValueError(f"Menu item at index {idx}: all keywords must be strings")

# Validate menu items when the module is loaded
try:
    validate_menu_items()
except ValueError as e:
    raise ValueError(f"Menu validation failed: {str(e)}")