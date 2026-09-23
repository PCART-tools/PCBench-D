    def repartition(self, npartitions):
        """ Coalesce bag into fewer partitions

        Examples
        --------
        >>> b.repartition(5)  # set to have 5 partitions  # doctest: +SKIP
        """
        if npartitions > self.npartitions:
            msg = ("Repartition only supports going to fewer partitions\n"
                   " old: %d  new: %d")
            raise NotImplementedError(msg % (self.npartitions, npartitions))
        npartitions_ratio = self.npartitions / npartitions
        new_partitions_boundaries = [int(old_partition_index * npartitions_ratio)
                                     for old_partition_index in range(npartitions + 1)]
        new_name = 'repartition-%d-%s' % (npartitions, tokenize(self))

        dsk = {}
        for new_partition_index in range(npartitions):
            value = (list, (toolz.concat,
                            [(self.name, old_partition_index)
                             for old_partition_index in
                             range(new_partitions_boundaries[new_partition_index],
                                   new_partitions_boundaries[new_partition_index + 1])]))
            dsk[new_name, new_partition_index] = value
        return Bag(dsk=merge(self.dask, dsk), name=new_name, npartitions=npartitions)
