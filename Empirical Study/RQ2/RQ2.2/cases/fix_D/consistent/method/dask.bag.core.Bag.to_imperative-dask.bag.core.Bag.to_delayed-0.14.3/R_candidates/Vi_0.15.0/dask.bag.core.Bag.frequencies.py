    def frequencies(self, split_every=None):
        """ Count number of occurrences of each distinct element

        >>> b = from_sequence(['Alice', 'Bob', 'Alice'])
        >>> dict(b.frequencies())  # doctest: +SKIP
        {'Alice': 2, 'Bob', 1}
        """
        return self.reduction(frequencies, merge_frequencies,
                              out_type=Bag, split_every=split_every,
                              name='frequencies').map_partitions(dictitems)
