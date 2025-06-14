def boyer_moore(text, pattern):
    m = len(pattern)
    n = len(text)
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
