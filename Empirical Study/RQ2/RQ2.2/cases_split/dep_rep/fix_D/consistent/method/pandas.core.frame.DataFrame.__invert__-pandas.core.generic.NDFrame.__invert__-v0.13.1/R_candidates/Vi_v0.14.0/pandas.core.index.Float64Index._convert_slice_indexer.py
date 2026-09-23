    def _convert_slice_indexer(self, key, typ=None):
        """ convert a slice indexer, by definition these are labels
            unless we are iloc """
        if typ == 'iloc':
            return super(Float64Index, self)._convert_slice_indexer(key, typ=typ)

        # allow floats here
        self._validate_slicer(
            key, lambda v: v is None or is_integer(v) or is_float(v))

        # translate to locations
        return self.slice_indexer(key.start, key.stop, key.step)
