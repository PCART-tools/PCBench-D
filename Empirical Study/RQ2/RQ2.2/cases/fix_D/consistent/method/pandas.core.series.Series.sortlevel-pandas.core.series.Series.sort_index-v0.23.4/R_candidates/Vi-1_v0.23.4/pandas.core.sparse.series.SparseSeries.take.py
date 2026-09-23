    @Appender(generic._shared_docs['take'])
    def take(self, indices, axis=0, convert=None, *args, **kwargs):
        if convert is not None:
            msg = ("The 'convert' parameter is deprecated "
                   "and will be removed in a future version.")
            warnings.warn(msg, FutureWarning, stacklevel=2)
        else:
            convert = True

        nv.validate_take_with_convert(convert, args, kwargs)
        new_values = SparseArray.take(self.values, indices)
        new_index = self.index.take(indices)
        return self._constructor(new_values,
                                 index=new_index).__finalize__(self)
