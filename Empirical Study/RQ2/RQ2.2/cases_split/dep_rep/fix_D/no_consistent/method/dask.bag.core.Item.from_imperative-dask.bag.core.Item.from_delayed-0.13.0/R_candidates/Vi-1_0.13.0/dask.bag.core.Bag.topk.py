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
