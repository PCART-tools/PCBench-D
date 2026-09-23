    def _convert_slice_indexer(self, key, typ=None):
        """ convert a slice indexer, by definition these are labels
            unless we are iloc """

        # if we are not a slice, then we are done
        if not isinstance(key, slice):
            return key

        if typ == 'iloc':
            return super(Float64Index, self)._convert_slice_indexer(key,
                                                                    typ=typ)

        # allow floats here
        validator = lambda v: v is None or is_integer(v) or is_float(v)
        self._validate_slicer(key, validator)

        # translate to locations
        return self.slice_indexer(key.start, key.stop, key.step)
