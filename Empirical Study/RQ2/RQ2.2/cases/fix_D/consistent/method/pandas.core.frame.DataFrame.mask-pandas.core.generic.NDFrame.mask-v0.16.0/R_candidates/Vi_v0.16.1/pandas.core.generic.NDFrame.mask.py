    @Appender(_shared_docs['where'] % dict(_shared_doc_kwargs, cond="False"))
    def mask(self, cond, other=np.nan, inplace=False, axis=None, level=None,
             try_cast=False, raise_on_error=True):
        return self.where(~cond, other=other, inplace=inplace, axis=axis,
            level=level, try_cast=try_cast, raise_on_error=raise_on_error)
