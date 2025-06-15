import time
import os
from typing import List, Dict, Tuple
from algorithms.KMP import kmp_search, kmp_search_all
from algorithms.BM import boyer_moore, boyer_moore_all
from algorithms.levenshtein import levenshtein_distance
from .ekstrak_regex import extract_regex, extract_details_regex

class CVMatcher:
    def __init__(self, similarity_threshold=0.8):
        self.similarity_threshold = similarity_threshold
        
    def extract_cv_text(self, cv_path: str) -> str:
        """Extract text from CV PDF"""
        if not os.path.exists(cv_path):            return ""
        return extract_regex(cv_path)
    
    def exact_match_search(self, text: str, keywords: List[str], algorithm: str) -> Dict:
        """Perform exact matching using specified algorithm"""
        start_time = time.time()
        matches = {}
        
        # Convert text to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        for keyword in keywords:
            keyword_lower = keyword.lower().strip()
            
            # Use the appropriate algorithm to find all occurrences
            if algorithm.upper() == 'KMP':
                positions = kmp_search_all(text_lower, keyword_lower)
            else:  # Boyer-Moore
                positions = boyer_moore_all(text_lower, keyword_lower)
            
            if positions:
                matches[keyword] = {
                    'count': len(positions),
                    'positions': positions
                }
        
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        return {
            'matches': matches,
            'execution_time': execution_time,
            'total_matches': sum(match['count'] for match in matches.values())
        }
    
    def fuzzy_match_search(self, text: str, keywords: List[str]) -> Dict:
        """Perform fuzzy matching using Levenshtein distance"""
        start_time = time.time()
        fuzzy_matches = {}
        
        # Split text into words for fuzzy matching
        words = text.lower().split()
        
        for keyword in keywords:
            keyword_lower = keyword.lower().strip()
            best_matches = []
            
            for word in words:
                # Calculate similarity
                distance = levenshtein_distance(keyword_lower, word)
                max_len = max(len(keyword_lower), len(word))
                
                if max_len > 0:
                    similarity = 1 - (distance / max_len)
                    
                    if similarity >= self.similarity_threshold:
                        best_matches.append({
                            'word': word,
                            'similarity': similarity,
                            'distance': distance
                        })
            
            if best_matches:
                # Sort by similarity (highest first)
                best_matches.sort(key=lambda x: x['similarity'], reverse=True)
                fuzzy_matches[keyword] = best_matches[:5]  # Keep top 5 matches
        
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        return {
            'fuzzy_matches': fuzzy_matches,
            'execution_time': execution_time
        }
    
    def search_cvs(self, cv_data_list: List[Dict], keywords: List[str], algorithm: str) -> Tuple[List[Dict], Dict]:
        """Search through all CVs and return ranked results"""
        results = []
        total_exact_time = 0
        total_fuzzy_time = 0
        total_cvs_scanned = len(cv_data_list)
        
        for cv_data in cv_data_list:
            cv_path = cv_data.get('cv_path', '')
            cv_text = self.extract_cv_text(cv_path)
            
            if not cv_text:
                continue
            
            # Perform exact matching
            exact_results = self.exact_match_search(cv_text, keywords, algorithm)
            total_exact_time += exact_results['execution_time']
            
            # Perform fuzzy matching for keywords not found in exact match
            unmatched_keywords = [kw for kw in keywords if kw not in exact_results['matches']]
            fuzzy_results = {'fuzzy_matches': {}, 'execution_time': 0}
            
            if unmatched_keywords:
                fuzzy_results = self.fuzzy_match_search(cv_text, unmatched_keywords)
                total_fuzzy_time += fuzzy_results['execution_time']
            
            # Calculate total score
            exact_score = exact_results['total_matches']
            fuzzy_score = len(fuzzy_results['fuzzy_matches'])
            total_score = exact_score + (fuzzy_score * 0.5)  # Weight fuzzy matches less
            
            if total_score > 0:  # Only include CVs with matches
                result_data = {
                    'cv_data': cv_data,
                    'exact_matches': exact_results['matches'],
                    'fuzzy_matches': fuzzy_results['fuzzy_matches'],
                    'total_score': total_score,
                    'exact_score': exact_score,
                    'fuzzy_score': fuzzy_score
                }
                results.append(result_data)
        
        # Sort by total score (highest first)
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        # Prepare timing information
        timing_info = {
            'exact_match_time': total_exact_time,
            'fuzzy_match_time': total_fuzzy_time,
            'total_cvs_scanned': total_cvs_scanned,
            'algorithm_used': algorithm
        }
        
        return results, timing_info
