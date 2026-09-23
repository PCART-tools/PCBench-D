class RuleSet(object):
    """A set of rewrite rules.

    Forms a structure for fast rewriting over a set of rewrite rules. This
    allows for syntactic matching of terms to patterns for many patterns at
    the same time.

    Examples
    --------

    >>> def f(*args): pass
    >>> def g(*args): pass
    >>> def h(*args): pass
    >>> from operator import add

    >>> rs = RuleSet(                 # Make RuleSet with two Rules
    ...         RewriteRule((add, 'x', 0), 'x', ('x',)),
    ...         RewriteRule((f, (g, 'x'), 'y'),
    ...                     (h, 'x', 'y'),
    ...                     ('x', 'y')))

    >>> rs.rewrite((add, 2, 0))       # Apply ruleset to single task
    2

    >>> rs.rewrite((f, (g, 'a', 3)))  # doctest: +SKIP
    (h, 'a', 3)

    >>> dsk = {'a': (add, 2, 0),      # Apply ruleset to full dask graph
    ...        'b': (f, (g, 'a', 3))}

    >>> from toolz import valmap
    >>> valmap(rs.rewrite, dsk)  # doctest: +SKIP
    {'a': 2,
     'b': (h, 'a', 3)}

    Attributes
    ----------
    rules : list
        A list of `RewriteRule`s included in the `RuleSet`.
    """

    def __init__(self, *rules):
        """Create a `RuleSet` for a number of rules

        Parameters
        ----------
        rules
            One or more instances of RewriteRule
        """
        self._net = Node()
        self.rules = []
        for p in rules:
            self.add(p)

    def add(self, rule):
        """Add a rule to the RuleSet.

        Parameters
        ----------
        rule : RewriteRule
        """

        if not isinstance(rule, RewriteRule):
            raise TypeError("rule must be instance of RewriteRule")
        vars = rule.vars
        curr_node = self._net
        ind = len(self.rules)
        # List of variables, in order they appear in the POT of the term
        for t in Traverser(rule.lhs):
            prev_node = curr_node
            if t in vars:
                t = VAR
            if t in curr_node.edges:
                curr_node = curr_node.edges[t]
            else:
                curr_node.edges[t] = Node()
                curr_node = curr_node.edges[t]
        # We've reached a leaf node. Add the term index to this leaf.
        prev_node.edges[t].patterns.append(ind)
        self.rules.append(rule)

    def iter_matches(self, term):
        """A generator that lazily finds matchings for term from the RuleSet.

        Parameters
        ----------
        term : task

        Yields
        ------
        Tuples of `(rule, subs)`, where `rule` is the rewrite rule being
        matched, and `subs` is a dictionary mapping the variables in the lhs
        of the rule to their matching values in the term."""

        S = Traverser(term)
        for m, syms in _match(S, self._net):
            for i in m:
                rule = self.rules[i]
                subs = _process_match(rule, syms)
                if subs is not None:
                    yield rule, subs

    def _rewrite(self, term):
        """Apply the rewrite rules in RuleSet to top level of term"""

        for rule, sd in self.iter_matches(term):
            # We use for (...) because it's fast in all cases for getting the
            # first element from the match iterator. As we only want that
            # element, we break here
            term = rule.subs(sd)
            break
        return term

    def rewrite(self, task, strategy="bottom_up"):
        """Apply the `RuleSet` to `task`.

        This applies the most specific matching rule in the RuleSet to the
        task, using the provided strategy.

        Parameters
        ----------
        term: a task
            The task to be rewritten
        strategy: str, optional
            The rewriting strategy to use. Options are "bottom_up" (default),
            or "top_level".

        Examples
        --------
        Suppose there was a function `add` that returned the sum of 2 numbers,
        and another function `double` that returned twice its input:

        >>> add = lambda x, y: x + y
        >>> double = lambda x: 2*x

        Now suppose `double` was *significantly* faster than `add`, so
        you'd like to replace all expressions `(add, x, x)` with `(double,
        x)`, where `x` is a variable. This can be expressed as a rewrite rule:

        >>> rule = RewriteRule((add, 'x', 'x'), (double, 'x'), ('x',))
        >>> rs = RuleSet(rule)

        This can then be applied to terms to perform the rewriting:

        >>> term = (add, (add, 2, 2), (add, 2, 2))
        >>> rs.rewrite(term)  # doctest: +SKIP
        (double, (double, 2))

        If we only wanted to apply this to the top level of the term, the
        `strategy` kwarg can be set to "top_level".

        >>> rs.rewrite(term)  # doctest: +SKIP
        (double, (add, 2, 2))
        """
        return strategies[strategy](self, task)
