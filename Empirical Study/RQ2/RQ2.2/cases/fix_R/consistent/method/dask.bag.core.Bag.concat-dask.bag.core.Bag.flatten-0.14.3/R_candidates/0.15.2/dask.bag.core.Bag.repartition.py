    def repartition(self, npartitions):
        """ Coalesce bag into fewer partitions

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
