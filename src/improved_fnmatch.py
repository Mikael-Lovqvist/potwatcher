import re

def translate(pat, double_star=False):
    """Translate a shell PATTERN to a regular expression.

    There is no way to quote meta-characters.
    """

    STAR = object()
    DOUBLE_STAR = object()
    res = []
    add = res.append
    i, n = 0, len(pat)
    while i < n:
        c = pat[i]
        i = i+1
        if c == '*':
            if double_star:
                # a consequtive `*` will be turned into a DOUBLE_STAR
                if res and res[-1] is STAR:
                    res[-1] = DOUBLE_STAR
                elif (not res) or res[-1] is not STAR:
                    add(STAR)
            else:
                # compress consecutive `*` into one
                if (not res) or res[-1] is not STAR:
                    add(STAR)
        elif c == '?':
            add('.')
        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                j = j+1
            if j < n and pat[j] == ']':
                j = j+1
            while j < n and pat[j] != ']':
                j = j+1
            if j >= n:
                add('\\[')
            else:
                stuff = pat[i:j]
                if '-' not in stuff:
                    stuff = stuff.replace('\\', r'\\')
                else:
                    chunks = []
                    k = i+2 if pat[i] == '!' else i+1
                    while True:
                        k = pat.find('-', k, j)
                        if k < 0:
                            break
                        chunks.append(pat[i:k])
                        i = k+1
                        k = k+3
                    chunk = pat[i:j]
                    if chunk:
                        chunks.append(chunk)
                    else:
                        chunks[-1] += '-'
                    # Remove empty ranges -- invalid in RE.
                    for k in range(len(chunks)-1, 0, -1):
                        if chunks[k-1][-1] > chunks[k][0]:
                            chunks[k-1] = chunks[k-1][:-1] + chunks[k][1:]
                            del chunks[k]
                    # Escape backslashes and hyphens for set difference (--).
                    # Hyphens that create ranges shouldn't be escaped.
                    stuff = '-'.join(s.replace('\\', r'\\').replace('-', r'\-')
                                     for s in chunks)
                # Escape set operations (&&, ~~ and ||).
                stuff = re.sub(r'([&~|])', r'\\\1', stuff)
                i = j+1
                if not stuff:
                    # Empty range: never match.
                    add('(?!)')
                elif stuff == '!':
                    # Negated empty range: match any character.
                    add('.')
                else:
                    if stuff[0] == '!':
                        stuff = '^' + stuff[1:]
                    elif stuff[0] in ('^', '['):
                        stuff = '\\' + stuff
                    add(f'[{stuff}]')
        else:
            add(re.escape(c))
    assert i == n

    # Deal with STARs.
    inp = res
    res = []
    add = res.append
    i, n = 0, len(inp)
    # Fixed pieces at the start?
    while i < n and inp[i] not in (STAR, DOUBLE_STAR):
        add(inp[i])
        i += 1
    # Now deal with STAR fixed STAR fixed ...
    # For an interior `STAR fixed` pairing, we want to do a minimal
    # .*? match followed by `fixed`, with no possibility of backtracking.
    # Atomic groups ("(?>...)") allow us to spell that directly.
    # Note: people rely on the undocumented ability to join multiple
    # translate() results together via "|" to build large regexps matching
    # "one of many" shell patterns.
    while i < n:
        if inp[i] is STAR:
            if double_star:
                star_expansion = r'[^/]*'
            else:
                star_expansion = r'.*'
        elif inp[i] is DOUBLE_STAR:
            star_expansion = r'.*'
        else:
            raise AssertionError()

        i += 1
        if i == n:
            add(star_expansion)
            break
        assert inp[i] not in (STAR, DOUBLE_STAR)
        fixed = []
        while i < n and inp[i] not in (STAR, DOUBLE_STAR):
            fixed.append(inp[i])
            i += 1
        fixed = "".join(fixed)
        if i == n:
            add(star_expansion)
            add(fixed)
        else:
            add(f"(?>{star_expansion}?{fixed})")
    assert i == n
    res = "".join(res)
    return fr'(?s:{res})\Z'
