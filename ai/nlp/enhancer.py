# ai/nlp/enhancer.py
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class SmartQueryEnhancer:
    def __init__(self):
        self.academic_context = {
            'semesters': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8'],
            'exam_types': ['regular', 'supplementary', 'revaluation'],
            'document_types': ['report', 'receipt', 'application', 'result']
        }

    def enhance_query(self, query: str, user_context: Dict = None) -> Dict[str, Any]:
        try:
            enhanced = {
                'original_query': query,
                'enhanced_terms': self._expand_academic_terms(query),
                'context': self._extract_context(query, user_context),
                'semantic_variations': self._generate_semantic_variations(query)
            }

            return enhanced

        except Exception as e:
            logger.error(f"Query enhancement failed: {e}")
            return {'error': str(e)}

    def _expand_academic_terms(self, query: str) -> List[str]:
        expansions = {
            'marks': ['grade', 'score', 'result', 'performance'],
            'exam': ['examination', 'test', 'assessment'],
            'payment': ['fee', 'amount', 'transaction'],
            'report': ['document', 'certificate', 'statement']
        }
        
        expanded_terms = []
        query_terms = query.lower().split()
        
        for term in query_terms:
            if term in expansions:
                expanded_terms.extend(expansions[term])
        
        return expanded_terms

    def _extract_context(self, query: str, user_context: Dict = None) -> Dict[str, Any]:
        context = {
            'semester': None,
            'exam_type': None,
            'document_type': None
        }

        query_lower = query.lower()
        
        # Extract semester
        for sem in self.academic_context['semesters']:
            if sem.lower() in query_lower:
                context['semester'] = sem
                break

        # Extract exam type
        for exam_type in self.academic_context['exam_types']:
            if exam_type in query_lower:
                context['exam_type'] = exam_type
                break

        # Extract document type
        for doc_type in self.academic_context['document_types']:
            if doc_type in query_lower:
                context['document_type'] = doc_type
                break

        # Merge with user context if available
        if user_context:
            context.update({k: v for k, v in user_context.items() if v is not None})

        return context

    def _generate_semantic_variations(self, query: str) -> List[str]:
        variations = []
        query_lower = query.lower()

        # Generate variations based on common patterns
        if 'check' in query_lower:
            variations.extend(['view', 'see', 'find'])
        if 'marks' in query_lower:
            variations.extend(['grade', 'result', 'score'])
        if 'exam' in query_lower:
            variations.extend(['test', 'assessment', 'evaluation'])

        return variations