def equivalent(term1, term2, subs=None):
    """Determine if two terms are equivalent, modulo variable substitution.

    Equivalent to applying substitutions in `subs` to `term2`, then checking if
    `term1 == term2`.

    If a subterm doesn't support comparison (i.e. `term1 == term2` errors),
    returns `False`.

    Parameters
    ----------
    term1, term2 : terms
    subs : dict, optional
        Mapping of substitutions from `term2` to `term1`

    Examples
    --------
    >>> from operator import add
    >>> term1 = (add, 'a', 'b')
    >>> term2 = (add, 'x', 'y')
    >>> subs = {'x': 'a', 'y': 'b'}
    >>> equivalent(term1, term2, subs)
    True
    >>> subs = {'x': 'a'}
    >>> equivalent(term1, term2, subs)
    False
    """

    # Quick escape for special cases
    head_type = type(term1)
    if type(term2) != head_type:
        # If terms aren't same type, fail
        return False
    elif head_type not in (tuple, list):
        # For literals, just compare
        try:
            # `is` is tried first, to allow objects that don't implement `==`
            # to work for cases where term1 is term2. If `is` returns False,
            # and `==` errors, then the only thing we can do is return False.
            return term1 is term2 or term1 == term2
        except:
            return False

    pot1 = preorder_traversal(term1)
    pot2 = preorder_traversal(term2)
    subs = {} if subs is None else subs

    for t1, t2 in zip_longest(pot1, pot2, fillvalue=END):
        if t1 is END or t2 is END:
            # If terms aren't same length: fail
            return False
        elif ishashable(t2) and t2 in subs:
            val = subs[t2]
        else:
            val = t2
        try:
            if t1 is not t2 and t1 != val:
                return False
        except:
            return False
    return True
