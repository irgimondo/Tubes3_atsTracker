def kmp_search(text, pattern):
    """
    KMP search algorithm that returns the first occurrence position
    Returns -1 if pattern is not found
    """
    m = len(pattern)
    n = len(text)
    
    if m == 0:
        return 0
    if m > n:
        return -1
    
    lps = [0] * m

    # Preprocessing the pattern to create lps array
    j = 0
    compute_lps(pattern, m, lps)

    # Matching phase
    i = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j  # Match found
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def kmp_search_all(text, pattern):
    """
    KMP search algorithm that returns all occurrence positions
    Returns list of positions where pattern is found
    """
    m = len(pattern)
    n = len(text)
    
    if m == 0:
        return [0]
    if m > n:
        return []
    
    lps = [0] * m
    positions = []

    # Preprocessing the pattern to create lps array
    j = 0
    compute_lps(pattern, m, lps)

    # Matching phase
    i = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            positions.append(i - j)  # Match found
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return positions

# Helper function to create lps (longest prefix suffix) array
def compute_lps(pattern, m, lps):
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
