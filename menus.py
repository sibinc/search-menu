# menus.py

# Query enhancers for semantic understanding
QUERY_ENHANCERS = {
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

MENUS = [
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
        "name": "supplementary Report",
        "description": "supplementary Report",
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
    }
]