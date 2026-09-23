    def reduction(self, perpartition, aggregate, split_every=None,
                  out_type=Item, name=None):
        """ Reduce collection with reduction operators

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
