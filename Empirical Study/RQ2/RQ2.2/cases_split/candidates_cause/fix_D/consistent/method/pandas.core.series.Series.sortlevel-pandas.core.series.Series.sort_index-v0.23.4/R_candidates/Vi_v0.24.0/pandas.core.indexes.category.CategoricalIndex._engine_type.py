    @property
    def _engine_type(self):
        # self.codes can have dtype int8, int16, int32 or int64, so we need
        # to return the corresponding engine type (libindex.Int8Engine, etc.).
        return {np.int8: libindex.Int8Engine,
                np.int16: libindex.Int16Engine,
                np.int32: libindex.Int32Engine,
                np.int64: libindex.Int64Engine,
                }[self.codes.dtype.type]
