    @Appender(_shared_docs['where'] % dict(_shared_doc_kwargs, cond="True",
                                           name='where', name_other='mask'))
    def where(self, cond, other=np.nan, inplace=False, axis=None, level=None,
              try_cast=False, raise_on_error=True):

        other = com._apply_if_callable(other, self)
        return self._where(cond, other, inplace, axis, level, try_cast,
                           raise_on_error)
