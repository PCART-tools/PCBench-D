    @Appender(_shared_docs['where'] % dict(_shared_doc_kwargs, cond="False",
                                           name='mask', name_other='where'))
    def mask(self, cond, other=np.nan, inplace=False, axis=None, level=None,
             try_cast=False, raise_on_error=True):

        inplace = validate_bool_kwarg(inplace, 'inplace')
        cond = com._apply_if_callable(cond, self)

        return self.where(~cond, other=other, inplace=inplace, axis=axis,
                          level=level, try_cast=try_cast,
                          raise_on_error=raise_on_error)
