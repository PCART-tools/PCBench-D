    def join(self, other, on_self, on_other=None):
        """ Join collection with another collection

        Other collection must be an Iterable, and not a Bag.

        >>> people = from_sequence(['Alice', 'Bob', 'Charlie'])
        >>> fruit = ['Apple', 'Apricot', 'Banana']
        >>> list(people.join(fruit, lambda x: x[0]))  # doctest: +SKIP
        [('Apple', 'Alice'), ('Apricot', 'Alice'), ('Banana', 'Bob')]
        """
        assert isinstance(other, Iterable)
        assert not isinstance(other, Bag)
        if on_other is None:
            on_other = on_self
        name = 'join-' + tokenize(self, other, on_self, on_other)
        dsk = dict(((name, i), (list, (join, on_other, other,
                                       on_self, (self.name, i))))
                   for i in range(self.npartitions))
        return type(self)(merge(self.dask, dsk), name, self.npartitions)
