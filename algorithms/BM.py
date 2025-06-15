def boyer_moore(text, pattern):
    """
    Boyer-Moore search algorithm that returns the first occurrence position
    Returns -1 if pattern is not found
    """
    m = len(pattern)
    n = len(text)
    
    if m == 0:
        return 0
    if m > n:
        return -1
    
    bad_char = [-1] * 256

    # Preprocess the pattern
    for i in range(m):
        bad_char[ord(pattern[i])] = i

    # Searching phase
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        else:
            s += max(1, j - bad_char[ord(text[s + j])])
    return -1

def boyer_moore_all(text, pattern):
    """
    Boyer-Moore search algorithm that returns all occurrence positions
    Returns list of positions where pattern is found
    """
    m = len(pattern)
    n = len(text)
    
    if m == 0:
        return [0]
    if m > n:
        return []
    
    bad_char = [-1] * 256
    positions = []

    # Preprocess the pattern
    for i in range(m):
        bad_char[ord(pattern[i])] = i

    # Searching phase
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            positions.append(s)
            s += max(1, m - bad_char[ord(text[s + m])] if s + m < n else 1)
        else:
            s += max(1, j - bad_char[ord(text[s + j])])
    
    return positions
