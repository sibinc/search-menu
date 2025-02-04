from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load the model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Sample features and their instructions/links
features = [
    {"feature": "Generate progress report for a student", 
     "instructions": "Click here to generate a progress report for a specific student based on their performance in all subjects.", 
     "link": "http://yourplatform.com/generate-progress-report"},
    
    {"feature": "View attendance details for a specific student", 
     "instructions": "Click here to view the attendance details for a specific student over the chosen time period.", 
     "link": "http://yourplatform.com/view-attendance"},
    
    {"feature": "Find a student by ID or name", 
     "instructions": "Click here to search for a student by their ID or name to view their profile and details.", 
     "link": "http://yourplatform.com/search-student"},
    
    {"feature": "View all marks for a specific semester", 
     "instructions": "Click here to view the marks of all students for a particular semester and course.", 
     "link": "http://yourplatform.com/view-semester-marks"},
    
    {"feature": "Generate consolidated mark card for multiple semesters", 
     "instructions": "Click here to generate a consolidated mark card showing the performance of a student across multiple semesters.", 
     "link": "http://yourplatform.com/generate-consolidated-mark-card"},
    
    {"feature": "Schedule an exam for a course", 
     "instructions": "Click here to schedule an upcoming exam for a specific course, including the date, time, and venue.", 
     "link": "http://yourplatform.com/schedule-exam"},
    
    {"feature": "Check student fee payment status", 
     "instructions": "Click here to check if a student has paid their fees for the current semester.", 
     "link": "http://yourplatform.com/check-fee-status"},
    
    {"feature": "Add new student to the system", 
     "instructions": "Click here to add a new student to the academic management system by entering their details.", 
     "link": "http://yourplatform.com/add-student"},
    
    {"feature": "View course details and syllabus", 
     "instructions": "Click here to view the detailed syllabus and course content for a specific subject or course.", 
     "link": "http://yourplatform.com/view-course-details"},
    
    {"feature": "Download exam hall ticket", 
     "instructions": "Click here to download the hall ticket for an upcoming exam after entering your details.", 
     "link": "http://yourplatform.com/download-hall-ticket"}
]

# Convert features to embeddings
feature_embeddings = model.encode([f['feature'] for f in features])

# Store embeddings in FAISS
dimension = feature_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(feature_embeddings))

# Function to search for the closest features
def search_feature(query, top_k=3, threshold=0.5):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k=top_k)

    # Gather results
    results = []
    for i, idx in enumerate(indices[0]):
        similarity_score = 1 - distances[0][i]  # Convert distance to similarity score
        if similarity_score >= threshold:
            results.append({
                "feature": features[idx]['feature'],
                "instructions": features[idx]['instructions'],
                "link": features[idx]['link'],
                "similarity_score": similarity_score
            })

    # If no results meet threshold, return a clarification prompt
    if not results:
        return {"message": "Sorry, we couldn't find a close match. Please clarify your query."}

    return results

# Test the function with a query
query = "regular semester mark card"
results = search_feature(query)
print("Search Results:", results)
