    def _maybe_box(self, values):
        """ genericically box the values """

        if isinstance(values, self.__class__):
            return values
        elif not hasattr(values, '__iter__'):
            v = lib.infer_dtype([values])
            if v == 'datetime':
                return lib.Timestamp(v)
            return values

        v = lib.infer_dtype(values)
        if v == 'datetime':
            return lib.map_infer(values, lib.Timestamp)

        if isinstance(values, np.ndarray):
            return self.__class__(values)

        return values
