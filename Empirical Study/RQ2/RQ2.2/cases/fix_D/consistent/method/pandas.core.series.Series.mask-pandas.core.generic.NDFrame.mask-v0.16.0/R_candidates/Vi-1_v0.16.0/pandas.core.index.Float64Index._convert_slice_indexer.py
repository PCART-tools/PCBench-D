    def _convert_slice_indexer(self, key, kind=None):
        """
        convert a slice indexer, by definition these are labels
        unless we are iloc

        Parameters
        ----------
        key : label of the slice bound
        kind : optional, type of the indexing operation (loc/ix/iloc/None)
        """

        # if we are not a slice, then we are done
        if not isinstance(key, slice):
            return key

        if kind == 'iloc':
            return super(Float64Index, self)._convert_slice_indexer(key,
                                                                    kind=kind)

        # translate to locations
        return self.slice_indexer(key.start, key.stop, key.step)
