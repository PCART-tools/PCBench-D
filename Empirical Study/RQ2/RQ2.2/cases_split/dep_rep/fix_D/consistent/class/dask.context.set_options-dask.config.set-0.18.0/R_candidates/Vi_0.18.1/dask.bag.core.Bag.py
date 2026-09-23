class Bag(DaskMethodsMixin):
    """ Parallel collection of Python objects

    Examples
    --------
    Create Bag from sequence

    >>> import dask.bag as db
    >>> b = db.from_sequence(range(5))
    >>> list(b.filter(lambda x: x % 2 == 0).map(lambda x: x * 10))  # doctest: +SKIP
    [0, 20, 40]

    Create Bag from filename or globstring of filenames

    >>> b = db.read_text('/path/to/mydata.*.json.gz').map(json.loads)  # doctest: +SKIP

    Create manually (expert use)

    >>> dsk = {('x', 0): (range, 5),
    ...        ('x', 1): (range, 5),
    ...        ('x', 2): (range, 5)}
    >>> b = Bag(dsk, 'x', npartitions=3)

    >>> sorted(b.map(lambda x: x * 10))  # doctest: +SKIP
    [0, 0, 0, 10, 10, 10, 20, 20, 20, 30, 30, 30, 40, 40, 40]

    >>> int(b.fold(lambda x, y: x + y))  # doctest: +SKIP
    30
    """
    def __init__(self, dsk, name, npartitions):
        self.dask = dsk
        self.name = name
        self.npartitions = npartitions

    def __dask_graph__(self):
        return self.dask

    def __dask_keys__(self):
        return [(self.name, i) for i in range(self.npartitions)]

    def __dask_tokenize__(self):
        return self.name

    __dask_optimize__ = globalmethod(optimize, key='bag_optimize',
                                     falsey=dont_optimize)
    __dask_scheduler__ = staticmethod(mpget)

    def __dask_postcompute__(self):
        return finalize, ()

    def __dask_postpersist__(self):
        return type(self), (self.name, self.npartitions)

    def __str__(self):
        name = self.name if len(self.name) < 10 else self.name[:7] + '...'
        return 'dask.bag<%s, npartitions=%d>' % (name, self.npartitions)

    __repr__ = __str__

    str = property(fget=StringAccessor)

    def map(self, func, *args, **kwargs):
        """Apply a function elementwise across one or more bags.

        Note that all ``Bag`` arguments must be partitioned identically.

        Parameters
        ----------
        func : callable
        *args, **kwargs : Bag, Item, or object
            Extra arguments and keyword arguments to pass to ``func`` *after*
            the calling bag instance. Non-Bag args/kwargs are broadcasted
            across all calls to ``func``.

        Notes
        -----
        For calls with multiple `Bag` arguments, corresponding partitions
        should have the same length; if they do not, the call will error at
        compute time.

        Examples
        --------
        >>> import dask.bag as db
        >>> b = db.from_sequence(range(5), npartitions=2)
        >>> b2 = db.from_sequence(range(5, 10), npartitions=2)

        Apply a function to all elements in a bag:

        >>> b.map(lambda x: x + 1).compute()
        [1, 2, 3, 4, 5]

        Apply a function with arguments from multiple bags:

        >>> from operator import add
        >>> b.map(add, b2).compute()
        [5, 7, 9, 11, 13]

        Non-bag arguments are broadcast across all calls to the mapped
        function:

        >>> b.map(add, 1).compute()
        [1, 2, 3, 4, 5]

        Keyword arguments are also supported, and have the same semantics as
        regular arguments:

        >>> def myadd(x, y=0):
        ...     return x + y
        >>> b.map(myadd, y=b2).compute()
        [5, 7, 9, 11, 13]
        >>> b.map(myadd, y=1).compute()
        [1, 2, 3, 4, 5]

        Both arguments and keyword arguments can also be instances of
        ``dask.bag.Item``. Here we'll add the max value in the bag to each
        element:

        >>> b.map(myadd, b.max()).compute()
        [4, 5, 6, 7, 8]
        """
        return bag_map(func, self, *args, **kwargs)

    def starmap(self, func, **kwargs):
        """Apply a function using argument tuples from the given bag.

        This is similar to ``itertools.starmap``, except it also accepts
        keyword arguments. In pseudocode, this is could be written as:

        >>> def starmap(func, bag, **kwargs):
        ...     return (func(*args, **kwargs) for args in bag)

        Parameters
        ----------
        func : callable
        **kwargs : Item, Delayed, or object, optional
            Extra keyword arguments to pass to ``func``. These can either be
            normal objects, ``dask.bag.Item``, or ``dask.delayed.Delayed``.

        Examples
        --------
        >>> import dask.bag as db
        >>> data = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
        >>> b = db.from_sequence(data, npartitions=2)

        Apply a function to each argument tuple:

        >>> from operator import add
        >>> b.starmap(add).compute()
        [3, 7, 11, 15, 19]

        Apply a function to each argument tuple, with additional keyword
        arguments:

        >>> def myadd(x, y, z=0):
        ...     return x + y + z
        >>> b.starmap(myadd, z=10).compute()
        [13, 17, 21, 25, 29]

        Keyword arguments can also be instances of ``dask.bag.Item`` or
        ``dask.delayed.Delayed``:

        >>> max_second = b.pluck(1).max()
        >>> max_second.compute()
        10
        >>> b.starmap(myadd, z=max_second).compute()
        [13, 17, 21, 25, 29]
        """
        name = 'starmap-{0}-{1}'.format(funcname(func),
                                        tokenize(self, func, kwargs))
        dsk = self.dask.copy()
        if kwargs:
            kw_dsk, kwargs = unpack_scalar_dask_kwargs(kwargs)
            dsk.update(kw_dsk)
        dsk.update({(name, i): (reify, (starmap_chunk, func, (self.name, i), kwargs))
                   for i in range(self.npartitions)})
        return type(self)(dsk, name, self.npartitions)

    @property
    def _args(self):
        return (self.dask, self.name, self.npartitions)

    def __getstate__(self):
        return self._args

    def __setstate__(self, state):
        self.dask, self.name, self.npartitions = state

    def filter(self, predicate):
        """ Filter elements in collection by a predicate function.

        >>> def iseven(x):
        ...     return x % 2 == 0

        >>> import dask.bag as db
        >>> b = db.from_sequence(range(5))
        >>> list(b.filter(iseven))  # doctest: +SKIP
        [0, 2, 4]
        """
        name = 'filter-{0}-{1}'.format(funcname(predicate),
                                       tokenize(self, predicate))
        dsk = dict(((name, i), (reify, (filter, predicate, (self.name, i))))
                   for i in range(self.npartitions))
        return type(self)(merge(self.dask, dsk), name, self.npartitions)

    def random_sample(self, prob, random_state=None):
        """ Return elements from bag with probability of ``prob``.

        Parameters
        ----------
        prob : float
            A float between 0 and 1, representing the probability that each
            element will be returned.
        random_state : int or random.Random, optional
            If an integer, will be used to seed a new ``random.Random`` object.
            If provided, results in deterministic sampling.

        Examples
        --------
        >>> import dask.bag as db
        >>> b = db.from_sequence(range(5))
        >>> list(b.random_sample(0.5, 42))
        [1, 4]
        >>> list(b.random_sample(0.5, 42))
        [1, 4]
        """
        if not 0 <= prob <= 1:
            raise ValueError('prob must be a number in the interval [0, 1]')
        if not isinstance(random_state, Random):
            random_state = Random(random_state)

        name = 'random-sample-%s' % tokenize(self, prob, random_state.getstate())
        state_data = random_state_data_python(self.npartitions, random_state)
        dsk = {(name, i): (reify, (random_sample, (self.name, i), state, prob))
               for i, state in zip(range(self.npartitions), state_data)}
        return type(self)(merge(self.dask, dsk), name, self.npartitions)

    def remove(self, predicate):
        """ Remove elements in collection that match predicate.

        >>> def iseven(x):
        ...     return x % 2 == 0

        >>> import dask.bag as db
        >>> b = db.from_sequence(range(5))
        >>> list(b.remove(iseven))  # doctest: +SKIP
        [1, 3]
        """
        name = 'remove-{0}-{1}'.format(funcname(predicate),
                                       tokenize(self, predicate))
        dsk = dict(((name, i), (reify, (remove, predicate, (self.name, i))))
                   for i in range(self.npartitions))
        return type(self)(merge(self.dask, dsk), name, self.npartitions)

    def map_partitions(self, func, *args, **kwargs):
        """Apply a function to every partition across one or more bags.

        Note that all ``Bag`` arguments must be partitioned identically.

        Parameters
        ----------
        func : callable
            The function to be called on every partition.
            This function should expect an ``Iterator`` or ``Iterable`` for
            every partition and should return an ``Iterator`` or ``Iterable``
            in return.
        *args, **kwargs : Bag, Item, Delayed, or object
            Arguments and keyword arguments to pass to ``func``.
            Partitions from this bag will be the first argument, and these will
            be passed *after*.

        Examples
        --------
        >>> import dask.bag as db
        >>> b = db.from_sequence(range(1, 101), npartitions=10)
        >>> def div(nums, den=1):
        ...     return [num / den for num in nums]

        Using a python object:

        >>> hi = b.max().compute()
        >>> hi
        100
        >>> b.map_partitions(div, den=hi).take(5)
        (0.01, 0.02, 0.03, 0.04, 0.05)

        Using an ``Item``:

        >>> b.map_partitions(div, den=b.max()).take(5)
        (0.01, 0.02, 0.03, 0.04, 0.05)

        Note that while both versions give the same output, the second forms a
        single graph, and then computes everything at once, and in some cases
        may be more efficient.
        """
        return map_partitions(func, self, *args, **kwargs)

    def pluck(self, key, default=no_default):
        """ Select item from all tuples/dicts in collection.

        >>> b = from_sequence([{'name': 'Alice', 'credits': [1, 2, 3]},
        ...                    {'name': 'Bob',   'credits': [10, 20]}])
        >>> list(b.pluck('name'))  # doctest: +SKIP
        ['Alice', 'Bob']
        >>> list(b.pluck('credits').pluck(0))  # doctest: +SKIP
        [1, 10]
        """
        name = 'pluck-' + tokenize(self, key, default)
        key = quote(key)
        if default == no_default:
            dsk = dict(((name, i), (list, (pluck, key, (self.name, i))))
                       for i in range(self.npartitions))
        else:
            dsk = dict(((name, i), (list, (pluck, key, (self.name, i), default)))
                       for i in range(self.npartitions))
        return type(self)(merge(self.dask, dsk), name, self.npartitions)

    def unzip(self, n):
        """Transform a bag of tuples to ``n`` bags of their elements.

        Examples
        --------
        >>> b = from_sequence([(i, i + 1, i + 2) for i in range(10)])
        >>> first, second, third = b.unzip(3)
        >>> isinstance(first, Bag)
        True
        >>> first.compute()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        Note that this is equivalent to:

        >>> first, second, third = (b.pluck(i) for i in range(3))
        """
        return tuple(self.pluck(i) for i in range(n))

    @wraps(to_textfiles)
    def to_textfiles(self, path, name_function=None, compression='infer',
                     encoding=system_encoding, compute=True,
                     storage_options=None, **kwargs):
        return to_textfiles(self, path, name_function, compression, encoding,
                            compute, storage_options=storage_options, **kwargs)

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
        if initial is not no_default:
            return self.reduction(curry(_reduce, binop, initial=initial),
                                  curry(_reduce, combine),
                                  split_every=split_every)
        else:
            from toolz.curried import reduce
            return self.reduction(reduce(binop), reduce(combine),
                                  split_every=split_every)

    def frequencies(self, split_every=None):
        """ Count number of occurrences of each distinct element.

        >>> b = from_sequence(['Alice', 'Bob', 'Alice'])
        >>> dict(b.frequencies())  # doctest: +SKIP
        {'Alice': 2, 'Bob', 1}
        """
        return self.reduction(frequencies, merge_frequencies,
                              out_type=Bag, split_every=split_every,
                              name='frequencies').map_partitions(dictitems)

    def topk(self, k, key=None, split_every=None):
        """ K largest elements in collection

        Optionally ordered by some key function

        >>> b = from_sequence([10, 3, 5, 7, 11, 4])
        >>> list(b.topk(2))  # doctest: +SKIP
        [11, 10]

        >>> list(b.topk(2, lambda x: -x))  # doctest: +SKIP
        [3, 4]
        """
        if key:
            if callable(key) and takes_multiple_arguments(key):
                key = partial(apply, key)
            func = partial(topk, k, key=key)
        else:
            func = partial(topk, k)
        return self.reduction(func, compose(func, toolz.concat), out_type=Bag,
                              split_every=split_every, name='topk')

    def distinct(self):
        """ Distinct elements of collection

        Unordered without repeats.

        >>> b = from_sequence(['Alice', 'Bob', 'Alice'])
        >>> sorted(b.distinct())
        ['Alice', 'Bob']
        """
        return self.reduction(set, merge_distinct, out_type=Bag,
                              name='distinct')

    def reduction(self, perpartition, aggregate, split_every=None,
                  out_type=Item, name=None):
        """ Reduce collection with reduction operators.

        Parameters
        ----------
        perpartition: function
            reduction to apply to each partition
        aggregate: function
            reduction to apply to the results of all partitions
        split_every: int (optional)
            Group partitions into groups of this size while performing reduction
            Defaults to 8
        out_type: {Bag, Item}
            The out type of the result, Item if a single element, Bag if a list
            of elements.  Defaults to Item.

        Examples
        --------
        >>> b = from_sequence(range(10))
        >>> b.reduction(sum, sum).compute()
        45
        """
        if split_every is None:
            split_every = 8
        if split_every is False:
            split_every = self.npartitions

        token = tokenize(self, perpartition, aggregate, split_every)
        a = '%s-part-%s' % (name or funcname(perpartition), token)
        is_last = self.npartitions == 1
        dsk = {(a, i): (empty_safe_apply, perpartition, (self.name, i), is_last)
               for i in range(self.npartitions)}
        k = self.npartitions
        b = a
        fmt = '%s-aggregate-%s' % (name or funcname(aggregate), token)
        depth = 0

        while k > split_every:
            c = fmt + str(depth)
            dsk2 = dict(((c, i), (empty_safe_aggregate, aggregate,
                                  [(b, j) for j in inds], False))
                        for i, inds in enumerate(partition_all(split_every,
                                                               range(k))))
            dsk.update(dsk2)
            k = len(dsk2)
            b = c
            depth += 1

        dsk[(fmt, 0)] = (empty_safe_aggregate, aggregate,
                         [(b, j) for j in range(k)], True)

        if out_type is Item:
            dsk[fmt] = dsk.pop((fmt, 0))
            return Item(merge(self.dask, dsk), fmt)
        else:
            return Bag(merge(self.dask, dsk), fmt, 1)

    def sum(self, split_every=None):
        """ Sum all elements """
        return self.reduction(sum, sum, split_every=split_every)

    def max(self, split_every=None):
        """ Maximum element """
        return self.reduction(max, max, split_every=split_every)

    def min(self, split_every=None):
        """ Minimum element """
        return self.reduction(min, min, split_every=split_every)

    def any(self, split_every=None):
        """ Are any of the elements truthy? """
        return self.reduction(any, any, split_every=split_every)

    def all(self, split_every=None):
        """ Are all elements truthy? """
        return self.reduction(all, all, split_every=split_every)

    def count(self, split_every=None):
        """ Count the number of elements. """
        return self.reduction(count, sum, split_every=split_every)

    def mean(self):
        """ Arithmetic mean """
        def mean_chunk(seq):
            total, n = 0.0, 0
            for x in seq:
                total += x
                n += 1
            return total, n

        def mean_aggregate(x):
            totals, counts = list(zip(*x))
            return 1.0 * sum(totals) / sum(counts)

        return self.reduction(mean_chunk, mean_aggregate, split_every=False)

    def var(self, ddof=0):
        """ Variance """
        def var_chunk(seq):
            squares, total, n = 0.0, 0.0, 0
            for x in seq:
                squares += x**2
                total += x
                n += 1
            return squares, total, n

        def var_aggregate(x):
            squares, totals, counts = list(zip(*x))
            x2, x, n = float(sum(squares)), float(sum(totals)), sum(counts)
            result = (x2 / n) - (x / n)**2
            return result * n / (n - ddof)

        return self.reduction(var_chunk, var_aggregate, split_every=False)

    def std(self, ddof=0):
        """ Standard deviation """
        return self.var(ddof=ddof).apply(math.sqrt)

    def join(self, other, on_self, on_other=None):
        """ Joins collection with another collection.

        Other collection must be one of the following:

        1.  An iterable.  We recommend tuples over lists for internal
            performance reasons.
        2.  A delayed object, pointing to a tuple.  This is recommended if the
            other collection is sizable and you're using the distributed
            scheduler.  Dask is able to pass around data wrapped in delayed
            objects with greater sophistication.
        3.  A Bag with a single partition

        You might also consider Dask Dataframe, whose join operations are much
        more heavily optimized.

        Parameters
        ----------
        other: Iterable, Delayed, Bag
            Other collection on which to join
        on_self: callable
            Function to call on elements in this collection to determine a
            match
        on_other: callable (defaults to on_self)
            Function to call on elements in the other collection to determine a
            match

        Examples
        --------
        >>> people = from_sequence(['Alice', 'Bob', 'Charlie'])
        >>> fruit = ['Apple', 'Apricot', 'Banana']
        >>> list(people.join(fruit, lambda x: x[0]))  # doctest: +SKIP
        [('Apple', 'Alice'), ('Apricot', 'Alice'), ('Banana', 'Bob')]
        """
        name = 'join-' + tokenize(self, other, on_self, on_other)
        dsk = {}
        if isinstance(other, Bag):
            if other.npartitions == 1:
                dsk.update(other.dask)
                other = other.__dask_keys__()[0]
                dsk['join-%s-other' % name] = (list, other)
            else:
                msg = ("Multi-bag joins are not implemented. "
                       "We recommend Dask dataframe if appropriate")
                raise NotImplementedError(msg)
        elif isinstance(other, Delayed):
            dsk.update(other.dask)
            other = other._key
        elif isinstance(other, Iterable):
            other = other
        else:
            msg = ("Joined argument must be single-partition Bag, "
                   " delayed object, or Iterable, got %s" %
                   type(other).__name)
            raise TypeError(msg)

        if on_other is None:
            on_other = on_self

        dsk.update({(name, i): (list, (join, on_other, other,
                                       on_self, (self.name, i)))
                   for i in range(self.npartitions)})
        return type(self)(merge(self.dask, dsk), name, self.npartitions)

    def product(self, other):
        """ Cartesian product between two bags. """
        assert isinstance(other, Bag)
        name = 'product-' + tokenize(self, other)
        n, m = self.npartitions, other.npartitions
        dsk = dict(((name, i * m + j),
                   (list, (itertools.product, (self.name, i),
                                              (other.name, j))))
                   for i in range(n) for j in range(m))
        return type(self)(merge(self.dask, other.dask, dsk), name, n * m)

    def foldby(self, key, binop, initial=no_default, combine=None,
               combine_initial=no_default, split_every=None):
        """ Combined reduction and groupby.

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

        **split_every**

        Group partitions into groups of this size while performing reduction.
        Defaults to 8.

        >>> b.foldby('name', binop, 0, combine, 0)  # doctest: +SKIP

        See Also
        --------

        toolz.reduceby
        pyspark.combineByKey
        """
        if split_every is None:
            split_every = 8
        if split_every is False:
            split_every = self.npartitions

        token = tokenize(self, key, binop, initial, combine, combine_initial)
        a = 'foldby-a-' + token
        if combine is None:
            combine = binop
        if initial is not no_default:
            dsk = {(a, i): (reduceby, key, binop, (self.name, i), initial)
                   for i in range(self.npartitions)}
        else:
            dsk = {(a, i): (reduceby, key, binop, (self.name, i))
                   for i in range(self.npartitions)}

        def combine2(acc, x):
            return combine(acc, x[1])

        depth = 0
        k = self.npartitions
        b = a
        while k > split_every:
            c = b + str(depth)
            if combine_initial is not no_default:
                dsk2 = {(c, i): (reduceby, 0, combine2,
                                 (toolz.concat, (map, dictitems,
                                                 [(b, j) for j in inds])),
                                 combine_initial)
                        for i, inds in enumerate(partition_all(split_every,
                                                               range(k)))}
            else:
                dsk2 = {(c, i): (merge_with, (partial, reduce, combine),
                                 [(b, j) for j in inds])
                        for i, inds in enumerate(partition_all(split_every,
                                                               range(k)))}
            dsk.update(dsk2)
            k = len(dsk2)
            b = c
            depth += 1

        e = 'foldby-b-' + token
        if combine_initial is not no_default:
            dsk[(e, 0)] = (dictitems, (reduceby, 0, combine2,
                                       (toolz.concat, (map, dictitems,
                                                       [(b, j) for j in range(k)])),
                                       combine_initial))
        else:
            dsk[(e, 0)] = (dictitems, (merge_with, (partial, reduce, combine),
                                       [(b, j) for j in range(k)]))

        return type(self)(merge(self.dask, dsk), e, 1)

    def take(self, k, npartitions=1, compute=True, warn=True):
        """ Take the first k elements.

        Parameters
        ----------
        k : int
            The number of elements to return
        npartitions : int, optional
            Elements are only taken from the first ``npartitions``, with a
            default of 1. If there are fewer than ``k`` rows in the first
            ``npartitions`` a warning will be raised and any found rows
            returned. Pass -1 to use all partitions.
        compute : bool, optional
            Whether to compute the result, default is True.
        warn : bool, optional
            Whether to warn if the number of elements returned is less than
            requested, default is True.

        >>> b = from_sequence(range(10))
        >>> b.take(3)  # doctest: +SKIP
        (0, 1, 2)
        """

        if npartitions <= -1:
            npartitions = self.npartitions
        if npartitions > self.npartitions:
            raise ValueError("only {} partitions, take "
                             "received {}".format(self.npartitions, npartitions))

        token = tokenize(self, k, npartitions)
        name = 'take-' + token

        if npartitions > 1:
            name_p = 'take-partial-' + token

            dsk = {}
            for i in range(npartitions):
                dsk[(name_p, i)] = (list, (take, k, (self.name, i)))

            concat = (toolz.concat, ([(name_p, i) for i in range(npartitions)]))
            dsk[(name, 0)] = (safe_take, k, concat, warn)
        else:
            dsk = {(name, 0): (safe_take, k, (self.name, 0), warn)}

        b = Bag(merge(self.dask, dsk), name, 1)

        if compute:
            return tuple(b.compute())
        else:
            return b

    def flatten(self):
        """ Concatenate nested lists into one long list.

        >>> b = from_sequence([[1], [2, 3]])
        >>> list(b)
        [[1], [2, 3]]

        >>> list(b.flatten())
        [1, 2, 3]
        """
        name = 'flatten-' + tokenize(self)
        dsk = dict(((name, i), (list, (toolz.concat, (self.name, i))))
                   for i in range(self.npartitions))
        return type(self)(merge(self.dask, dsk), name, self.npartitions)

    def __iter__(self):
        return iter(self.compute())

    def groupby(self, grouper, method=None, npartitions=None, blocksize=2**20,
                max_branch=None, shuffle=None):
        """ Group collection by key function

        This requires a full dataset read, serialization and shuffle.
        This is expensive.  If possible you should use ``foldby``.

        Parameters
        ----------
        grouper: function
            Function on which to group elements
        shuffle: str
            Either 'disk' for an on-disk shuffle or 'tasks' to use the task
            scheduling framework.  Use 'disk' if you are on a single machine
            and 'tasks' if you are on a distributed cluster.
        npartitions: int
            If using the disk-based shuffle, the number of output partitions
        blocksize: int
            If using the disk-based shuffle, the size of shuffle blocks (bytes)
        max_branch: int
            If using the task-based shuffle, the amount of splitting each
            partition undergoes.  Increase this for fewer copies but more
            scheduler overhead.

        Examples
        --------
        >>> b = from_sequence(range(10))
        >>> iseven = lambda x: x % 2 == 0
        >>> dict(b.groupby(iseven))  # doctest: +SKIP
        {True: [0, 2, 4, 6, 8], False: [1, 3, 5, 7, 9]}

        See Also
        --------
        Bag.foldby
        """
        if method is not None:
            raise Exception("The method= keyword has been moved to shuffle=")
        if shuffle is None:
            shuffle = config.get('shuffle', None)
        if shuffle is None:
            if 'distributed' in config.get('scheduler', ''):
                shuffle = 'tasks'
            else:
                shuffle = 'disk'
        if shuffle == 'disk':
            return groupby_disk(self, grouper, npartitions=npartitions,
                                blocksize=blocksize)
        elif shuffle == 'tasks':
            return groupby_tasks(self, grouper, max_branch=max_branch)
        else:
            msg = "Shuffle must be 'disk' or 'tasks'"
            raise NotImplementedError(msg)

    def to_dataframe(self, meta=None, columns=None):
        """ Create Dask Dataframe from a Dask Bag.

        Bag should contain tuples, dict records, or scalars.

        Index will not be particularly meaningful.  Use ``reindex`` afterwards
        if necessary.

        Parameters
        ----------
        meta : pd.DataFrame, dict, iterable, optional
            An empty ``pd.DataFrame`` that matches the dtypes and column names
            of the output. This metadata is necessary for many algorithms in
            dask dataframe to work.  For ease of use, some alternative inputs
            are also available. Instead of a ``DataFrame``, a ``dict`` of
            ``{name: dtype}`` or iterable of ``(name, dtype)`` can be provided.
            If not provided or a list, a single element from the first
            partition will be computed, triggering a potentially expensive call
            to ``compute``. This may lead to unexpected results, so providing
            ``meta`` is recommended. For more information, see
            ``dask.dataframe.utils.make_meta``.
        columns : sequence, optional
            Column names to use. If the passed data do not have names
            associated with them, this argument provides names for the columns.
            Otherwise this argument indicates the order of the columns in the
            result (any names not found in the data will become all-NA
            columns).  Note that if ``meta`` is provided, column names will be
            taken from there and this parameter is invalid.

        Examples
        --------
        >>> import dask.bag as db
        >>> b = db.from_sequence([{'name': 'Alice',   'balance': 100},
        ...                       {'name': 'Bob',     'balance': 200},
        ...                       {'name': 'Charlie', 'balance': 300}],
        ...                      npartitions=2)
        >>> df = b.to_dataframe()

        >>> df.compute()
           balance     name
        0      100    Alice
        1      200      Bob
        0      300  Charlie
        """
        import pandas as pd
        import dask.dataframe as dd
        if meta is None:
            if isinstance(columns, pd.DataFrame):
                warnings.warn("Passing metadata to `columns` is deprecated. "
                              "Please use the `meta` keyword instead.")
                meta = columns
            else:
                head = self.take(1, warn=False)
                if len(head) == 0:
                    raise ValueError("`dask.bag.Bag.to_dataframe` failed to "
                                     "properly infer metadata, please pass in "
                                     "metadata via the `meta` keyword")
                meta = pd.DataFrame(list(head), columns=columns)
        elif columns is not None:
            raise ValueError("Can't specify both `meta` and `columns`")
        else:
            meta = dd.utils.make_meta(meta)
        # Serializing the columns and dtypes is much smaller than serializing
        # the empty frame
        cols = list(meta.columns)
        dtypes = meta.dtypes.to_dict()
        name = 'to_dataframe-' + tokenize(self, cols, dtypes)
        dsk = self.__dask_optimize__(self.dask, self.__dask_keys__())
        dsk.update({(name, i): (to_dataframe, (self.name, i), cols, dtypes)
                    for i in range(self.npartitions)})
        divisions = [None] * (self.npartitions + 1)
        return dd.DataFrame(dsk, name, meta, divisions)

    def to_delayed(self, optimize_graph=True):
        """Convert into a list of ``dask.delayed`` objects, one per partition.

        Parameters
        ----------
        optimize_graph : bool, optional
            If True [default], the graph is optimized before converting into
            ``dask.delayed`` objects.

        See Also
        --------
        dask.bag.from_delayed
        """
        from dask.delayed import Delayed
        keys = self.__dask_keys__()
        dsk = self.__dask_graph__()
        if optimize_graph:
            dsk = self.__dask_optimize__(dsk, keys)
        return [Delayed(k, dsk) for k in keys]

    def repartition(self, npartitions):
        """ Coalesce bag into fewer partitions.

        Examples
        --------
        >>> b.repartition(5)  # set to have 5 partitions  # doctest: +SKIP
        """
        new_name = 'repartition-%d-%s' % (npartitions, tokenize(self, npartitions))
        if npartitions == self.npartitions:
            return self
        elif npartitions < self.npartitions:
            ratio = self.npartitions / npartitions
            new_partitions_boundaries = [int(old_partition_index * ratio)
                                         for old_partition_index in range(npartitions + 1)]

            dsk = {}
            for new_partition_index in range(npartitions):
                value = (list, (toolz.concat,
                                [(self.name, old_partition_index)
                                 for old_partition_index in
                                 range(new_partitions_boundaries[new_partition_index],
                                       new_partitions_boundaries[new_partition_index + 1])]))
                dsk[new_name, new_partition_index] = value
        else:  # npartitions > self.npartitions
            ratio = npartitions / self.npartitions
            split_name = 'split-%s' % tokenize(self, npartitions)
            dsk = {}
            last = 0
            j = 0
            for i in range(self.npartitions):
                new = last + ratio
                if i == self.npartitions - 1:
                    k = npartitions - j
                else:
                    k = int(new - last)
                dsk[(split_name, i)] = (split, (self.name, i), k)
                for jj in range(k):
                    dsk[(new_name, j)] = (getitem, (split_name, i), jj)
                    j += 1
                last = new

        return Bag(dsk=merge(self.dask, dsk), name=new_name, npartitions=npartitions)

    def accumulate(self, binop, initial=no_default):
        """ Repeatedly apply binary function to a sequence, accumulating results.

        This assumes that the bag is ordered.  While this is typically the case
        not all Dask.bag functions preserve this property.

        Examples
        --------
        >>> from operator import add
        >>> b = from_sequence([1, 2, 3, 4, 5], npartitions=2)
        >>> b.accumulate(add).compute()  # doctest: +SKIP
        [1, 3, 6, 10, 15]

        Accumulate also takes an optional argument that will be used as the
        first value.

        >>> b.accumulate(add, initial=-1)  # doctest: +SKIP
        [-1, 0, 2, 5, 9, 14]
        """
        if not _implement_accumulate:
            raise NotImplementedError("accumulate requires `toolz` > 0.7.4"
                                      " or `cytoolz` > 0.7.3.")
        token = tokenize(self, binop, initial)
        binop_name = funcname(binop)
        a = '%s-part-%s' % (binop_name, token)
        b = '%s-first-%s' % (binop_name, token)
        c = '%s-second-%s' % (binop_name, token)
        dsk = {(a, 0): (accumulate_part, binop, (self.name, 0), initial, True),
               (b, 0): (first, (a, 0)),
               (c, 0): (second, (a, 0))}
        for i in range(1, self.npartitions):
            dsk[(a, i)] = (accumulate_part, binop, (self.name, i), (c, i - 1))
            dsk[(b, i)] = (first, (a, i))
            dsk[(c, i)] = (second, (a, i))
        return Bag(merge(self.dask, dsk), b, self.npartitions)
