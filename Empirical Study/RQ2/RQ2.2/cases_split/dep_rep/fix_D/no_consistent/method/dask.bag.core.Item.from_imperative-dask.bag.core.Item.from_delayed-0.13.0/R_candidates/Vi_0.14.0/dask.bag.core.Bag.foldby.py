    def foldby(self, key, binop, initial=no_default, combine=None,
               combine_initial=no_default):
        """ Combined reduction and groupby

        Foldby provides a combined groupby and reduce for efficient parallel
        split-apply-combine tasks.

        The computation

        >>> b.foldby(key, binop, init)                        # doctest: +SKIP

        is equivalent to the following:

        >>> def reduction(group):                               # doctest: +SKIP
        ...     return reduce(binop, group, init)               # doctest: +SKIP

        >>> b.groupby(key).map(lambda (k, v): (k, reduction(v)))# doctest: +SKIP

        But uses minimal communication and so is *much* faster.

        >>> b = from_sequence(range(10))
        >>> iseven = lambda x: x % 2 == 0
        >>> add = lambda x, y: x + y
        >>> dict(b.foldby(iseven, add))                         # doctest: +SKIP
        {True: 20, False: 25}

        **Key Function**

        The key function determines how to group the elements in your bag.
        In the common case where your bag holds dictionaries then the key
        function often gets out one of those elements.

        >>> def key(x):
        ...     return x['name']

        This case is so common that it is special cased, and if you provide a
        key that is not a callable function then dask.bag will turn it into one
        automatically.  The following are equivalent:

        >>> b.foldby(lambda x: x['name'], ...)  # doctest: +SKIP
        >>> b.foldby('name', ...)  # doctest: +SKIP

        **Binops**

        It can be tricky to construct the right binary operators to perform
        analytic queries.  The ``foldby`` method accepts two binary operators,
        ``binop`` and ``combine``.  Binary operators two inputs and output must
        have the same type.

        Binop takes a running total and a new element and produces a new total:

        >>> def binop(total, x):
        ...     return total + x['amount']

        Combine takes two totals and combines them:

        >>> def combine(total1, total2):
        ...     return total1 + total2

        Each of these binary operators may have a default first value for
        total, before any other value is seen.  For addition binary operators
        like above this is often ``0`` or the identity element for your
        operation.

        >>> b.foldby('name', binop, 0, combine, 0)  # doctest: +SKIP

        See Also
        --------

        toolz.reduceby
        pyspark.combineByKey
        """
        token = tokenize(self, key, binop, initial, combine, combine_initial)
        a = 'foldby-a-' + token
        b = 'foldby-b-' + token
        if combine is None:
            combine = binop
        if initial is not no_default:
            dsk = dict(((a, i), (reduceby, key, binop, (self.name, i), initial))
                       for i in range(self.npartitions))
        else:
            dsk = dict(((a, i), (reduceby, key, binop, (self.name, i)))
                       for i in range(self.npartitions))

        def combine2(acc, x):
            return combine(acc, x[1])

        if combine_initial is not no_default:
            dsk2 = {(b, 0): (dictitems, (reduceby, 0, combine2,
                                         (toolz.concat, (map, dictitems,
                                                         list(dsk.keys()))),
                                         combine_initial))}
        else:
            dsk2 = {(b, 0): (dictitems, (merge_with, (partial, reduce, combine),
                                         list(dsk.keys())))}
        return type(self)(merge(self.dask, dsk, dsk2), b, 1)
