# services/search_service.py
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from ai.nlp.analyzer import QueryAnalyzer
from ai.nlp.enhancer import SmartQueryEnhancer
from ai.ml.ranker import AdaptiveRanker
from services.menu_service import MenuService
from services.storage_service import MenuStorage

from utils.logger import get_logger

logger = get_logger()

class SearchService:
    def __init__(self):
        """Initialize search service with AI components"""
        try:
            # Core services
            self.storage = MenuStorage()
            self.menu_service = MenuService(self.storage)
            
            # AI components
            self.query_analyzer = QueryAnalyzer()
            self.query_enhancer = SmartQueryEnhancer()
            self.ranker = AdaptiveRanker()
            
            logger.info("SearchService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize SearchService: {e}")
            raise

    async def search(self, 
                    query: str, 
                    user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Enhanced search with AI-powered analysis and ranking"""
        try:
            search_start_time = datetime.utcnow()
            
            # Step 1: Analyze query
            query_analysis = self.query_analyzer.analyze_query(query)
            logger.debug(f"Query analysis completed: {query_analysis}")
            
            # Step 2: Enhance query
            enhanced_query = self.query_enhancer.enhance_query(query, user_context)
            logger.debug(f"Query enhancement completed: {enhanced_query}")
            
            # Step 3: Get base results
            base_results = self.menu_service.get_all_menus()
            
            # Step 4: Apply AI ranking
            ranked_results = self.ranker.rank_results(
                base_results,
                query_analysis,
                user_context
            )
            
            search_time = (datetime.utcnow() - search_start_time).total_seconds()
            logger.info(f"Search completed in {search_time}s with {len(ranked_results)} results")
            
            return {
                'results': ranked_results,
                'metadata': {
                    'query': query,
                    'enhanced_query': enhanced_query,
                    'analysis': query_analysis,
                    'total_results': len(ranked_results),
                    'search_time': search_time,
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Search operation failed: {str(e)}")
            return {
                'results': [],
                'metadata': {
                    'error': str(e),
                    'query': query,
                    'timestamp': datetime.utcnow().isoformat()
                }
            }

    def record_user_interaction(self, 
                              query: str, 
                              selected_result: Dict,
                              user_context: Optional[Dict] = None):
        """Record user interactions for continuous learning"""
        try:
            self.ranker.update_from_feedback(query, selected_result)
            logger.info(
                f"User interaction recorded - Query: {query}, "
                f"Selected Result: {selected_result['id']}"
            )
        except Exception as e:
            logger.error(f"Failed to record user interaction: {str(e)}")

    def get_search_suggestions(self, 
                             partial_query: str,
                             user_context: Optional[Dict] = None) -> List[str]:
        """Get smart search suggestions based on partial query"""
        try:
            enhanced = self.query_enhancer.enhance_query(partial_query, user_context)
            suggestions = list(set([
                *enhanced['semantic_variations'],
                *enhanced['enhanced_terms']
            ]))[:5]
            
            logger.debug(f"Generated {len(suggestions)} suggestions for '{partial_query}'")
            return suggestions
            
        except Exception as e:
            logger.error(f"Failed to get search suggestions: {str(e)}")
            return []