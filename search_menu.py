# search-menu.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from menus import MENUS, QUERY_ENHANCERS

# ANSI Colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
RESET = "\033[0m"

class SearchEngine:
    def __init__(self):
        # Load model
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        print("Model loaded successfully!")
        
        # Prepare enhanced semantic texts for each menu item
        self.menu_semantic_texts = []
        for menu in MENUS:
            semantic_text = f"{menu['name']} {menu['description']} {menu['context']} {' '.join(menu['keywords'])}"
            self.menu_semantic_texts.append(semantic_text)
        
        # Create embeddings
        self.menu_embeddings = self.model.encode(self.menu_semantic_texts)
        
        # Store embeddings in FAISS
        self.dimension = self.menu_embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(np.array(self.menu_embeddings))
        print("Enhanced semantic embeddings stored in FAISS!")

    def preprocess_query(self, query):
        """Enhance query with semantic understanding"""
        enhanced_query = query
        
        # Add semantic enhancements from query enhancers
        for key, enhancer in QUERY_ENHANCERS.items():
            if key in query.lower():
                enhanced_query += f" {enhancer}"
        
        return enhanced_query

    def search(self, query):
        """
        Enhanced semantic search with better context understanding
        """
        if not query.strip():
            return None, None
        
        # Preprocess and enhance the query
        enhanced_query = self.preprocess_query(query)
        
        # Get embeddings for enhanced query
        query_embedding = self.model.encode([enhanced_query])
        
        # Get top 3 results and their distances
        distances, indices = self.index.search(np.array(query_embedding), k=3)
        
        # Convert distances to similarity scores (0-1 scale)
        similarities = 1 / (1 + distances[0])
        
        # Dynamic threshold based on best match
        best_similarity = max(similarities)
        threshold = max(0.5, best_similarity * 0.7)  # At least 70% as good as best match
        
        valid_results = []
        valid_scores = []
        
        for idx, similarity in enumerate(similarities):
            if similarity > threshold:
                result = MENUS[indices[0][idx]]
                # Add relevance info to help user understand why this was matched
                result['matched_keywords'] = [
                    kw for kw in result['keywords'] 
                    if kw.lower() in enhanced_query.lower()
                ]
                valid_results.append(result)
                valid_scores.append(similarity)
        
        if not valid_results:
            return None, None
        
        return valid_results, valid_scores

def print_results(results, scores):
    """Print formatted search results with enhanced information"""
    if not results:
        print(f"\n{RED}No matching results found. Please try a different search term.{RESET}")
        print(f"{YELLOW}You can try:{RESET}")
        print(f"{CYAN}- Using different keywords or synonyms")
        print("- Describing what you want to do")
        print("- Using natural language questions")
        print(f"- Being more specific about the type of report{RESET}")
        return

    print(f"\n{YELLOW}Found Results:{RESET}")
    print(f"{YELLOW}-------------{RESET}")
    
    for result, score in zip(results, scores):
        confidence = int(score * 100)
        print(f"{GREEN}Match Confidence: {CYAN}{confidence}%{RESET}")
        print(f"{GREEN}Name: {CYAN}{result['name']}{RESET}")
        print(f"{GREEN}Description: {CYAN}{result['description']}{RESET}")
        print(f"{GREEN}Context: {CYAN}{result['context']}{RESET}")
        if result.get('matched_keywords'):
            print(f"{GREEN}Matched Terms: {CYAN}{', '.join(result['matched_keywords'])}{RESET}")
        print(f"{GREEN}URL: {BLUE}{result['url']}{RESET}")
        print(f"{YELLOW}-------------{RESET}")

def main():
    search_engine = SearchEngine()
    
    print(f"\n{CYAN}Welcome to the Enhanced Report Search System!")
    print(f"You can search using natural language or keywords.")
    print(f"Examples:")
    print(f"- 'I need to get my paper rechecked'")
    print(f"- 'Where can I see my question-wise marks?'")
    print(f"- 'Need report for online evaluation'")
    print(f"Type your search query or 'quit' to exit{RESET}")
    
    while True:
        try:
            query = input(f"\n{GREEN}Enter search query >{RESET} ").strip()
            
            if not query:
                print(f"{RED}Please enter a search term.{RESET}")
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print(f"{YELLOW}Goodbye!{RESET}")
                break
            
            results, scores = search_engine.search(query)
            print_results(results, scores)
            
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Search cancelled. Goodbye!{RESET}")
            break
        except Exception as e:
            print(f"{RED}An error occurred: {str(e)}{RESET}")
            continue

if __name__ == "__main__":
    main()