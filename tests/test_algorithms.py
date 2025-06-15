"""
Test script to verify KMP, Boyer-Moore, and Levenshtein algorithms
"""

from algorithms.KMP import kmp_search, kmp_search_all
from algorithms.BM import boyer_moore, boyer_moore_all
from algorithms.levenshtein import levenshtein_distance

def test_kmp():
    """Test KMP algorithm"""
    print("Testing KMP Algorithm:")
    
    text = "hello world hello python hello"
    pattern = "hello"
    
    # Test single search
    pos = kmp_search(text, pattern)
    print(f"  Single search '{pattern}' in '{text}': position {pos}")
    
    # Test multiple search
    positions = kmp_search_all(text, pattern)
    print(f"  Multiple search '{pattern}' in '{text}': positions {positions}")
    
    # Test not found
    pos = kmp_search(text, "xyz")
    print(f"  Search 'xyz' in '{text}': position {pos}")
    
    print()

def test_boyer_moore():
    """Test Boyer-Moore algorithm"""
    print("Testing Boyer-Moore Algorithm:")
    
    text = "hello world hello python hello"
    pattern = "hello"
    
    # Test single search
    pos = boyer_moore(text, pattern)
    print(f"  Single search '{pattern}' in '{text}': position {pos}")
    
    # Test multiple search
    positions = boyer_moore_all(text, pattern)
    print(f"  Multiple search '{pattern}' in '{text}': positions {positions}")
    
    # Test not found
    pos = boyer_moore(text, "xyz")
    print(f"  Search 'xyz' in '{text}': position {pos}")
    
    print()

def test_levenshtein():
    """Test Levenshtein Distance algorithm"""
    print("Testing Levenshtein Distance:")
    
    test_cases = [
        ("python", "python"),  # Same strings
        ("python", "pyton"),   # Missing character
        ("python", "pythons"), # Extra character
        ("python", "java"),    # Different strings
        ("react", "reach"),    # Substitution
        ("javascript", "javscript"), # Transposition
    ]
    
    for str1, str2 in test_cases:
        distance = levenshtein_distance(str1, str2)
        max_len = max(len(str1), len(str2))
        similarity = 1 - (distance / max_len) if max_len > 0 else 1
        print(f"  '{str1}' vs '{str2}': distance={distance}, similarity={similarity:.2f}")
    
    print()

def test_case_sensitivity():
    """Test case sensitivity handling"""
    print("Testing Case Sensitivity:")
    
    text = "Hello World HELLO python Hello"
    pattern = "hello"
    
    # Test case-sensitive search
    pos_kmp = kmp_search(text, pattern)
    pos_bm = boyer_moore(text, pattern)
    print(f"  Case-sensitive search '{pattern}' in '{text}':")
    print(f"    KMP: {pos_kmp}, BM: {pos_bm}")
    
    # Test case-insensitive search
    pos_kmp_lower = kmp_search(text.lower(), pattern.lower())
    pos_bm_lower = boyer_moore(text.lower(), pattern.lower())
    print(f"  Case-insensitive search '{pattern}' in '{text.lower()}':")
    print(f"    KMP: {pos_kmp_lower}, BM: {pos_bm_lower}")
    
    print()

def test_performance():
    """Basic performance test"""
    print("Testing Performance (basic):")
    
    import time
    
    # Create a larger test text
    text = "python java javascript react vue angular node express django flask " * 1000
    pattern = "python"
    
    # Test KMP
    start = time.time()
    positions = kmp_search_all(text, pattern)
    kmp_time = (time.time() - start) * 1000
    
    # Test Boyer-Moore
    start = time.time()
    positions_bm = boyer_moore_all(text, pattern)
    bm_time = (time.time() - start) * 1000
    
    print(f"  Text length: {len(text)} characters")
    print(f"  Pattern: '{pattern}'")
    print(f"  KMP found {len(positions)} matches in {kmp_time:.2f}ms")
    print(f"  BM found {len(positions_bm)} matches in {bm_time:.2f}ms")
    
    print()

def main():
    """Run all tests"""
    print("=== ATS Algorithm Tests ===\n")
    
    test_kmp()
    test_boyer_moore()
    test_levenshtein()
    test_case_sensitivity()
    test_performance()
    
    print("=== All Tests Completed ===")

if __name__ == "__main__":
    main()
