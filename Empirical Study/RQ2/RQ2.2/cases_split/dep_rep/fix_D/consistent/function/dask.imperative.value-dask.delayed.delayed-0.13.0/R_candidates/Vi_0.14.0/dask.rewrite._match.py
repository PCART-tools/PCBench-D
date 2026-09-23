def _match(S, N):
    """Structural matching of term S to discrimination net node N."""

    stack = deque()
    restore_state_flag = False
    # matches are stored in a tuple, because all mutations result in a copy,
    # preventing operations from changing matches stored on the stack.
    matches = ()
    while True:
        if S.current is END:
            yield N.patterns, matches
        try:
            # This try-except block is to catch hashing errors from un-hashable
            # types. This allows for variables to be matched with un-hashable
            # objects.
            n = N.edges.get(S.current, None)
            if n and not restore_state_flag:
                stack.append((S.copy(), N, matches))
                N = n
                S.next()
                continue
        except TypeError:
            pass
        n = N.edges.get(VAR, None)
        if n:
            restore_state_flag = False
            matches = matches + (S.term,)
            S.skip()
            N = n
            continue
        try:
            # Backtrack here
            (S, N, matches) = stack.pop()
            restore_state_flag = True
        except:
            return
