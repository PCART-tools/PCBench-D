class RewriteRule(object):
    """A rewrite rule.

    Expresses `lhs` -> `rhs`, for variables `vars`.

    Parameters
    ----------
    lhs : task
        The left-hand-side of the rewrite rule.
    rhs : task or function
        The right-hand-side of the rewrite rule. If it's a task, variables in
        `rhs` will be replaced by terms in the subject that match the variables
        in `lhs`. If it's a function, the function will be called with a dict
        of such matches.
    vars: tuple, optional
        Tuple of variables found in the lhs. Variables can be represented as
        any hashable object; a good convention is to use strings. If there are
        no variables, this can be omitted.

    Examples
    --------
    Here's a `RewriteRule` to replace all nested calls to `list`, so that
    `(list, (list, 'x'))` is replaced with `(list, 'x')`, where `'x'` is a
    variable.

    >>> lhs = (list, (list, 'x'))
    >>> rhs = (list, 'x')
    >>> variables = ('x',)
    >>> rule = RewriteRule(lhs, rhs, variables)

    Here's a more complicated rule that uses a callable right-hand-side. A
    callable `rhs` takes in a dictionary mapping variables to their matching
    values. This rule replaces all occurrences of `(list, 'x')` with `'x'` if
    `'x'` is a list itself.

    >>> lhs = (list, 'x')
    >>> def repl_list(sd):
    ...     x = sd['x']
    ...     if isinstance(x, list):
    ...         return x
    ...     else:
    ...         return (list, x)
    >>> rule = RewriteRule(lhs, repl_list, variables)
    """

    def __init__(self, lhs, rhs, vars=()):
        if not isinstance(vars, tuple):
            raise TypeError("vars must be a tuple of variables")
        self.lhs = lhs
        if callable(rhs):
            self.subs = rhs
        else:
            self.subs = self._apply
        self.rhs = rhs
        self._varlist = [t for t in Traverser(lhs) if t in vars]
        # Reduce vars down to just variables found in lhs
        self.vars = tuple(sorted(set(self._varlist)))

    def _apply(self, sub_dict):
        term = self.rhs
        for key, val in sub_dict.items():
            term = subs(term, key, val)
        return term

    def __str__(self):
        return "RewriteRule({0}, {1}, {2})".format(self.lhs, self.rhs,
                                                   self.vars)

    def __repr__(self):
        return str(self)
