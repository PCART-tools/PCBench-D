    def fold(self, binop, combine=None, initial=no_default, split_every=None):
        """ Parallelizable reduction

        Fold is like the builtin function ``reduce`` except that it works in
        parallel.  Fold takes two binary operator functions, one to reduce each
        partition of our dataset and another to combine results between
        partitions

        1.  ``binop``: Binary operator to reduce within each partition
        2.  ``combine``:  Binary operator to combine results from binop

        Sequentially this would look like the following:

        >>> intermediates = [reduce(binop, part) for part in partitions]  # doctest: +SKIP
        >>> final = reduce(combine, intermediates)  # doctest: +SKIP

        If only one function is given then it is used for both functions
        ``binop`` and ``combine`` as in the following example to compute the
        sum:

        >>> def add(x, y):
        ...     return x + y

        >>> b = from_sequence(range(5))
        >>> b.fold(add).compute()  # doctest: +SKIP
        10

        In full form we provide both binary operators as well as their default
        arguments

        >>> b.fold(binop=add, combine=add, initial=0).compute()  # doctest: +SKIP
        10

        More complex binary operators are also doable

        >>> def add_to_set(acc, x):
        ...     ''' Add new element x to set acc '''
        ...     return acc | set([x])
        >>> b.fold(add_to_set, set.union, initial=set()).compute()  # doctest: +SKIP
        {1, 2, 3, 4, 5}

        See Also
        --------

        Bag.foldby
        """
        combine = combine or binop
        initial = quote(initial)
        if initial is not no_default:
            return self.reduction(curry(_reduce, binop, initial=initial),
                                  curry(_reduce, combine),
                                  split_every=split_every)
        else:
            from toolz.curried import reduce
            return self.reduction(reduce(binop), reduce(combine),
                                  split_every=split_every)
