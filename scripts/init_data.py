# init_data.py

import json
import os
from pathlib import Path

# Create data directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Initial menus data
initial_menus = [
    {
        "id": "revaluation-report",
        "name": "Revaluation Report",
        "description": "Revaluation EVALUATION_REPORT",
        "url": "revaluation-report",
        "keywords": [
            "recheck marks",
            "review evaluation",
            "reassessment"
        ],
        "context": "Used when students want their answer sheets to be evaluated again",
        "category": "evaluation",
        "order": 1,
        "active": True,
        "created_at": "2025-02-04T02:15:01Z",
        "updated_at": "2025-02-04T02:15:01Z"
    }
]

# Initial query enhancers
initial_query_enhancers = {
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
    "paper": "answer sheet exam script"
}

# Write initial menus data
with open(data_dir / "menus.json", "w") as f:
    json.dump(initial_menus, f, indent=2)

# Write initial query enhancers
with open(data_dir / "query_enhancers.json", "w") as f:
    json.dump(initial_query_enhancers, f, indent=2)

print("Data files initialized successfully!")