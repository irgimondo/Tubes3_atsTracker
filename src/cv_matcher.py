import time
import os
from typing import List, Dict, Tuple
from algorithms.KMP import kmp_search, kmp_search_all
from algorithms.BM import boyer_moore, boyer_moore_all
from algorithms.levenshtein import levenshtein_distance
from .ekstrak_regex import extract_regex, extract_details_regex
from database.database import DatabaseConnection

class CVMatcher:
    def __init__(self, similarity_threshold=0.8):
        self.similarity_threshold = similarity_threshold
        self.db = DatabaseConnection(password='root')
        
    def extract_cv_text(self, cv_path: str) -> str:
        """Extract text from CV PDF"""
        # Handle relative paths from database
        if not os.path.isabs(cv_path):
            # Normalize path separators and join with data directory
            normalized_path = cv_path.replace('\\', os.sep).replace('/', os.sep)
            full_path = os.path.join('data', normalized_path)
        else:
            full_path = cv_path
            
        if not os.path.exists(full_path):
            return ""
        return extract_regex(full_path)
    
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
            'time_taken': execution_time,  # For backwards compatibility
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
    
    def calculate_relevance_score(self, exact_matches: Dict, fuzzy_matches: Dict, keywords: List[str]) -> float:
        """Calculate comprehensive relevance score for ranking"""
        exact_score = 0
        fuzzy_score = 0
        keyword_coverage = 0
        
        # Calculate exact match score (higher weight)
        for keyword in keywords:
            if keyword in exact_matches:
                count = exact_matches[keyword]['count']
                # Diminishing returns for multiple occurrences
                exact_score += min(count * 2.0, 5.0)  # Max 5 points per keyword
        
        # Calculate fuzzy match score (lower weight)
        for keyword in keywords:
            if keyword in fuzzy_matches and fuzzy_matches[keyword]:
                best_match = fuzzy_matches[keyword][0]  # Take best match
                similarity = best_match['similarity']
                # Only count if similarity is high enough
                if similarity > 0.6:
                    fuzzy_score += similarity * 1.5  # Lower weight than exact
        
        # Keyword coverage bonus (percentage of keywords found)
        found_keywords = set()
        found_keywords.update(exact_matches.keys())
        found_keywords.update(fuzzy_matches.keys())
        
        if keywords:
            keyword_coverage = len(found_keywords) / len(keywords)
            coverage_bonus = keyword_coverage * 3.0  # Up to 3 points for full coverage
        else:
            coverage_bonus = 0
        
        # Calculate total score with weights
        total_score = (exact_score * 1.0) + (fuzzy_score * 0.7) + (coverage_bonus * 0.5)
        
        return round(total_score, 2)
    
    def rank_results(self, results: List[Dict], top_n: int = None) -> List[Dict]:
        """Rank results by relevance score and return top N"""
        # Sort by total score (descending)
        ranked_results = sorted(results, key=lambda x: x['total_score'], reverse=True)
        
        # Apply top N filter
        if top_n and top_n > 0:
            ranked_results = ranked_results[:top_n]
        
        return ranked_results
    
    def search_cvs(self, cv_data_list: List[Dict], keywords: List[str], algorithm: str, top_n: int = None) -> Tuple[List[Dict], Dict]:
        """Search through all CVs and return ranked results"""
        results = []
        total_exact_time = 0
        total_fuzzy_time = 0
        total_cvs_scanned = len(cv_data_list)        
        for cv_item in cv_data_list:
            cv_path = cv_item.get('cv_path', '')
            cv_text = self.extract_cv_text(cv_path)
            
            if not cv_text:
                continue
            
            # Perform exact matching
            exact_result = self.exact_match_search(cv_text, keywords, algorithm)
            exact_matches = exact_result['matches']
            total_exact_time += exact_result['time_taken']
            
            # Perform fuzzy matching for keywords not found exactly
            unfound_keywords = [kw for kw in keywords if kw not in exact_matches or not exact_matches[kw]]
            fuzzy_result = self.fuzzy_match_search(cv_text, unfound_keywords)
            fuzzy_matches = fuzzy_result['fuzzy_matches']
            total_fuzzy_time += fuzzy_result['execution_time']
            
            # Calculate comprehensive score
            total_score = self.calculate_relevance_score(exact_matches, fuzzy_matches, keywords)
            
            # Only include results with meaningful scores
            if total_score > 0:
                # Count matches for display
                exact_count = sum(info['count'] for info in exact_matches.values())
                fuzzy_count = len([k for k, v in fuzzy_matches.items() if v])
                
                result = {
                    'cv_data': cv_item,
                    'exact_matches': exact_matches,
                    'fuzzy_matches': fuzzy_matches,
                    'exact_score': exact_count,
                    'fuzzy_score': fuzzy_count,
                    'total_score': total_score,
                    'cv_text': cv_text[:500] + '...' if len(cv_text) > 500 else cv_text  # Preview
                }
                
                results.append(result)
        
        # Rank and filter results
        ranked_results = self.rank_results(results, top_n)
          # Timing information
        timing_info = {
            'exact_match_time': total_exact_time / 1000,  # Convert to seconds
            'fuzzy_match_time': total_fuzzy_time / 1000,  # Convert to seconds
            'total_cvs_scanned': total_cvs_scanned,
            'algorithm_used': algorithm,
            'results_returned': len(ranked_results)
        }
        
        return ranked_results, timing_info
    
    def get_all_applicants(self) -> List[Dict]:
        """Get all applicants from database"""
        try:
            if not self.db.connect():
                return []
            
            query = """
            SELECT ap.applicant_id, ap.first_name, ap.last_name, ap.email, ap.phone_number,
                   ap.summary, ap.skills, ap.experience, ap.education,
                   ad.application_role, ad.cv_path, ad.application_status
            FROM ApplicantProfile ap
            JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
            ORDER BY ap.first_name, ap.last_name
            """
            
            results = self.db.execute_query(query)
            self.db.disconnect()
            return results if results else []
            
        except Exception as e:
            print(f"Error getting applicants: {e}")
            return []
    
    def search_applicants_kmp(self, keyword: str, limit: int = 50) -> List[Dict]:
        """Search applicants using KMP algorithm"""
        return self._search_applicants_with_algorithm(keyword, 'KMP', limit)
    
    def search_applicants_boyer_moore(self, keyword: str, limit: int = 50) -> List[Dict]:
        """Search applicants using Boyer-Moore algorithm"""
        return self._search_applicants_with_algorithm(keyword, 'BM', limit)
    
    def search_applicants_fuzzy(self, keyword: str, limit: int = 50, threshold: float = None) -> List[Dict]:
        """Search applicants using fuzzy matching (Levenshtein distance)"""
        if threshold is None:
            threshold = self.similarity_threshold
            
        applicants = self.get_all_applicants()
        matches = []
        
        keyword_lower = keyword.lower().strip()
        
        for applicant in applicants:
            # Combine all searchable text
            searchable_text = " ".join([
                str(applicant.get('first_name', '')),
                str(applicant.get('last_name', '')),
                str(applicant.get('application_role', '')),
                str(applicant.get('summary', '')),
                str(applicant.get('skills', '')),
                str(applicant.get('experience', '')),
                str(applicant.get('education', ''))
            ]).lower()
            
            # Split into words for fuzzy matching
            words = searchable_text.split()
            best_similarity = 0
            best_word = ""
            
            for word in words:
                if len(word) < 2:  # Skip very short words
                    continue
                    
                distance = levenshtein_distance(keyword_lower, word)
                max_len = max(len(keyword_lower), len(word))
                
                if max_len > 0:
                    similarity = 1 - (distance / max_len)
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_word = word
            
            if best_similarity >= threshold:
                applicant['similarity_score'] = best_similarity
                applicant['matched_word'] = best_word
                matches.append(applicant)
        
        # Sort by similarity score (highest first)
        matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return matches[:limit]
    
    def _search_applicants_with_algorithm(self, keyword: str, algorithm: str, limit: int) -> List[Dict]:
        """Internal method to search applicants with specified algorithm"""
        applicants = self.get_all_applicants()
        matches = []
        
        keyword_lower = keyword.lower().strip()
        
        for applicant in applicants:
            # Combine all searchable text
            searchable_text = " ".join([
                str(applicant.get('first_name', '')),
                str(applicant.get('last_name', '')),
                str(applicant.get('application_role', '')),
                str(applicant.get('summary', '')),
                str(applicant.get('skills', '')),
                str(applicant.get('experience', '')),
                str(applicant.get('education', ''))
            ]).lower()
            
            # Use the specified algorithm to search
            if algorithm == 'KMP':
                positions = kmp_search_all(searchable_text, keyword_lower)
            else:  # Boyer-Moore
                positions = boyer_moore_all(searchable_text, keyword_lower)
            
            if positions:
                applicant['match_count'] = len(positions)
                applicant['match_positions'] = positions
                matches.append(applicant)
        
        # Sort by match count (highest first)
        matches.sort(key=lambda x: x['match_count'], reverse=True)
        
        return matches[:limit]
