# search_menu.py
from typing import List, Dict, Tuple, Optional
import logging
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from config.settings import SEARCH_CONFIG, COLORS
from services.menu_service import MenuService
from services.storage_service import MenuStorage

logger = logging.getLogger(__name__)

class SearchEngineError(Exception):
    """Base exception for search engine errors"""
    pass

class SearchEngine:
    def __init__(self):
        """Initialize the search engine"""
        try:
            self.storage = MenuStorage()
            self.menu_service = MenuService(self.storage)
            self.query_enhancers = self.storage.load_query_enhancers()
            
            # Load model
            self.model = SentenceTransformer(SEARCH_CONFIG['model_name'])
            logger.info("Model loaded successfully")
            
            # Prepare semantic texts and embeddings
            self._prepare_embeddings()
            
        except Exception as e:
            logger.error(f"Failed to initialize search engine: {e}")
            raise SearchEngineError(f"Search engine initialization failed: {e}")

    def _prepare_embeddings(self):
        """Prepare embeddings for all menu items"""
        try:
            menus = self.menu_service.get_all_menus()
            self.menu_semantic_texts = []
            
            for menu in menus:
                semantic_text = f"{menu.name} {menu.description} {menu.context} {' '.join(menu.keywords)}"
                self.menu_semantic_texts.append(semantic_text)
            
            # Create embeddings
            self.menu_embeddings = self.model.encode(self.menu_semantic_texts)
            
            # Store embeddings in FAISS
            self.dimension = self.menu_embeddings.shape[1]
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(np.array(self.menu_embeddings))
            
            logger.info("Enhanced semantic embeddings stored in FAISS")
            
        except Exception as e:
            logger.error(f"Failed to prepare embeddings: {e}")
            raise SearchEngineError(f"Failed to prepare embeddings: {e}")

    def _enhance_query(self, query: str) -> str:
        """Enhance query with semantic understanding"""
        enhanced_query = query
        
        for key, enhancer in self.query_enhancers.items():
            if key in query.lower():
                enhanced_query += f" {enhancer}"
        
        return enhanced_query

    def search(self, query: str) -> Tuple[Optional[List[Dict]], Optional[List[float]]]:
        """
        Perform semantic search
        
        Args:
            query: Search query string
            
        Returns:
            Tuple of (results, scores) or (None, None) if no results
        """
        try:
            if not query.strip():
                return None, None
            
            # Enhance query
            enhanced_query = self._enhance_query(query)
            logger.debug(f"Enhanced query: {enhanced_query}")
            
            # Get embeddings for query
            query_embedding = self.model.encode([enhanced_query])
            
            # Search
            distances, indices = self.index.search(
                np.array(query_embedding), 
                k=SEARCH_CONFIG['max_results']
            )
            
            # Process results
            similarities = 1 / (1 + distances[0])
            best_similarity = max(similarities)
            threshold = max(0.5, best_similarity * SEARCH_CONFIG['threshold_multiplier'])
            
            valid_results = []
            valid_scores = []
            menus = self.menu_service.get_all_menus()
            
            for idx, similarity in enumerate(similarities):
                if similarity > threshold:
                    menu = menus[indices[0][idx]]
                    result = menu.model_dump()
                    result['matched_keywords'] = [
                        kw for kw in menu.keywords 
                        if kw.lower() in enhanced_query.lower()
                    ]
                    valid_results.append(result)
                    valid_scores.append(similarity)
            
            logger.info(f"Search completed with {len(valid_results)} results")
            return (valid_results, valid_scores) if valid_results else (None, None)
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise SearchEngineError(f"Search failed: {e}")

def print_results(results: Optional[List[Dict]], scores: Optional[List[float]]) -> None:
    """Print formatted search results"""
    if not results:
        print(f"\n{COLORS['RED']}No matching results found. Please try a different search term.{COLORS['RESET']}")
        print(f"{COLORS['YELLOW']}You can try:{COLORS['RESET']}")
        print(f"{COLORS['CYAN']}- Using different keywords or synonyms")
        print("- Describing what you want to do")
        print("- Using natural language questions")
        print(f"- Being more specific about the type of report{COLORS['RESET']}")
        return

    print(f"\n{COLORS['YELLOW']}Found Results:{COLORS['RESET']}")
    print(f"{COLORS['YELLOW']}-------------{COLORS['RESET']}")
    
    for result, score in zip(results, scores):
        confidence = int(score * 100)
        print(f"{COLORS['GREEN']}Match Confidence: {COLORS['CYAN']}{confidence}%{COLORS['RESET']}")
        print(f"{COLORS['GREEN']}Name: {COLORS['CYAN']}{result['name']}{COLORS['RESET']}")
        print(f"{COLORS['GREEN']}Description: {COLORS['CYAN']}{result['description']}{COLORS['RESET']}")
        print(f"{COLORS['GREEN']}Context: {COLORS['CYAN']}{result['context']}{COLORS['RESET']}")
        if result.get('matched_keywords'):
            print(f"{COLORS['GREEN']}Matched Terms: {COLORS['CYAN']}{', '.join(result['matched_keywords'])}{COLORS['RESET']}")
        print(f"{COLORS['GREEN']}URL: {COLORS['BLUE']}{result['url']}{COLORS['RESET']}")
        print(f"{COLORS['YELLOW']}-------------{COLORS['RESET']}")

def main():
    """Main function"""
    try:
        search_engine = SearchEngine()
        
        print(f"\n{COLORS['CYAN']}Welcome to the Enhanced Report Search System!")
        print(f"You can search using natural language or keywords.")
        print(f"Examples:")
        print(f"- 'I need to get my paper rechecked'")
        print(f"- 'Where can I see my question-wise marks?'")
        print(f"- 'Need report for online evaluation'")
        print(f"Type your search query or 'quit' to exit{COLORS['RESET']}")
        
        while True:
            try:
                query = input(f"\n{COLORS['GREEN']}Enter search query >{COLORS['RESET']} ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print(f"{COLORS['YELLOW']}Goodbye!{COLORS['RESET']}")
                    break
                
                results, scores = search_engine.search(query)
                print_results(results, scores)
                
            except KeyboardInterrupt:
                print(f"\n{COLORS['YELLOW']}Search cancelled. Goodbye!{COLORS['RESET']}")
                break
            except Exception as e:
                logger.error(f"Error during search: {e}")
                print(f"{COLORS['RED']}An error occurred. Please try again.{COLORS['RESET']}")
    
    except Exception as e:
        logger.critical(f"Critical error: {e}")
        print(f"{COLORS['RED']}Failed to initialize search engine. Please check the logs.{COLORS['RESET']}")

if __name__ == "__main__":
    main()