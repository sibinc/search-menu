# ai/ml/ranker.py
from typing import List, Dict, Any
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AdaptiveRanker:
    def __init__(self):
        self.feedback_buffer = []
        self.ranking_weights = {
            'keyword_match': 0.3,
            'semantic_similarity': 0.3,
            'temporal_relevance': 0.2,
            'user_context': 0.2
        }

    def rank_results(self, 
                    results: List[Dict], 
                    query_analysis: Dict,
                    user_context: Dict = None) -> List[Dict]:
        try:
            ranked_results = []
            
            for result in results:
                score = self._calculate_ranking_score(
                    result, 
                    query_analysis,
                    user_context
                )
                ranked_results.append({
                    **result,
                    'ranking_score': score
                })

            # Sort by ranking score
            ranked_results.sort(key=lambda x: x['ranking_score'], reverse=True)
            
            return ranked_results

        except Exception as e:
            logger.error(f"Ranking failed: {e}")
            return results  # Return original results if ranking fails

    def _calculate_ranking_score(self, 
                               result: Dict, 
                               query_analysis: Dict,
                               user_context: Dict = None) -> float:
        try:
            scores = {
                'keyword_match': self._calculate_keyword_score(
                    result, 
                    query_analysis
                ),
                'semantic_similarity': self._calculate_semantic_score(
                    result, 
                    query_analysis
                ),
                'temporal_relevance': self._calculate_temporal_score(
                    result,
                    user_context
                ),
                'user_context': self._calculate_context_score(
                    result,
                    user_context
                )
            }

            # Calculate weighted sum
            final_score = sum(
                scores[key] * self.ranking_weights[key] 
                for key in scores
            )

            return final_score

        except Exception as e:
            logger.error(f"Score calculation failed: {e}")
            return 0.0

    def _calculate_keyword_score(self, 
                               result: Dict, 
                               query_analysis: Dict) -> float:
        # Simple keyword matching score
        keywords = query_analysis.get('enhanced_terms', [])
        if not keywords:
            return 0.0

        result_text = f"{result.get('name', '')} {result.get('description', '')}"
        matches = sum(1 for keyword in keywords if keyword in result_text.lower())
        return matches / len(keywords)

    def _calculate_semantic_score(self, 
                                result: Dict, 
                                query_analysis: Dict) -> float:
        # Use the confidence score from query analysis
        return query_analysis.get('confidence', 0.5)

    def _calculate_temporal_score(self, 
                                result: Dict,
                                user_context: Dict = None) -> float:
        if not user_context:
            return 0.5

        current_semester = user_context.get('current_semester')
        result_semester = result.get('semester')

        if current_semester and result_semester:
            if current_semester == result_semester:
                return 1.0
            return 0.5

        return 0.5

    def _calculate_context_score(self, 
                               result: Dict,
                               user_context: Dict = None) -> float:
        if not user_context:
            return 0.5

        score = 0.5
        if user_context.get('course') == result.get('course'):
            score += 0.25
        if user_context.get('exam_type') == result.get('exam_type'):
            score += 0.25

        return min(score, 1.0)

    def update_from_feedback(self, query: str, selected_result: Dict):
        """Learn from user feedback"""
        self.feedback_buffer.append((query, selected_result))
        
        if len(self.feedback_buffer) >= 100:
            self._update_ranking_weights()
            self.feedback_buffer = []

    def _update_ranking_weights(self):
        """Update ranking weights based on feedback"""
        if not self.feedback_buffer:
            return

        # Simple weight adjustment based on successful matches
        successful_matches = {
            'keyword_match': 0,
            'semantic_similarity': 0,
            'temporal_relevance': 0,
            'user_context': 0
        }

        total_matches = len(self.feedback_buffer)

        for query, result in self.feedback_buffer:
            if result.get('keyword_match_score', 0) > 0.7:
                successful_matches['keyword_match'] += 1
            if result.get('semantic_score', 0) > 0.7:
                successful_matches['semantic_similarity'] += 1
            if result.get('temporal_score', 0) > 0.7:
                successful_matches['temporal_relevance'] += 1
            if result.get('context_score', 0) > 0.7:
                successful_matches['user_context'] += 1

        # Update weights based on success rates
        for key in self.ranking_weights:
            success_rate = successful_matches[key] / total_matches
            self.ranking_weights[key] = (
                self.ranking_weights[key] * 0.8 + 
                success_rate * 0.2
            )

        # Normalize weights
        total_weight = sum(self.ranking_weights.values())
        for key in self.ranking_weights:
            self.ranking_weights[key] /= total_weight