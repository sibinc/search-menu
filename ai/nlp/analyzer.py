# ai/nlp/analyzer.py
from typing import Dict, Any
from transformers import pipeline
import logging

from utils.logger import get_logger

logger = get_logger()

class QueryAnalyzer:
    def __init__(self):
        try:
            self.classifier = pipeline(
                "text-classification",
                model="distilbert-base-uncased",
                return_all_scores=True
            )
        except Exception as e:
            logger.error(f"Failed to initialize QueryAnalyzer: {e}")
            raise

    def analyze_query(self, query: str) -> Dict[str, Any]:
        try:
            # Identify key academic terms
            academic_terms = {
                'revaluation': ['recheck', 'reeval', 'review'],
                'results': ['marks', 'grade', 'score', 'performance'],
                'examination': ['exam', 'test', 'assessment'],
                'payment': ['fee', 'amount', 'pay', 'receipt']
            }

            # Analyze query intent
            intent_scores = self.classifier(query)
            primary_intent = max(intent_scores[0], key=lambda x: x['score'])

            analysis = {
                'intent': primary_intent['label'],
                'confidence': primary_intent['score'],
                'academic_context': self._extract_academic_context(query, academic_terms),
                'query_type': self._determine_query_type(query)
            }

            return analysis

        except Exception as e:
            logger.error(f"Query analysis failed: {e}")
            return {'error': str(e)}

    def _extract_academic_context(self, query: str, terms: Dict) -> Dict[str, Any]:
        context = {}
        query_lower = query.lower()
        
        for category, keywords in terms.items():
            if any(term in query_lower for term in keywords):
                context[category] = True

        return context

    def _determine_query_type(self, query: str) -> str:
        query_lower = query.lower()
        if any(word in query_lower for word in ['how', 'what', 'why', 'when']):
            return 'question'
        elif any(word in query_lower for word in ['find', 'search', 'look', 'need']):
            return 'search'
        else:
            return 'statement'