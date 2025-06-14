def kmp_search(text, pattern):
    m = len(pattern)
    n = len(text)
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
