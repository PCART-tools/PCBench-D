    @Appender(_shared_docs['take'])
    def take(self, indices, axis=0, convert=None, is_copy=True, **kwargs):
        if convert is not None:
            msg = ("The 'convert' parameter is deprecated "
                   "and will be removed in a future version.")
            warnings.warn(msg, FutureWarning, stacklevel=2)
        else:
            convert = True

        convert = nv.validate_take(tuple(), kwargs)
        return self._take(indices, axis=axis, convert=convert, is_copy=is_copy)
