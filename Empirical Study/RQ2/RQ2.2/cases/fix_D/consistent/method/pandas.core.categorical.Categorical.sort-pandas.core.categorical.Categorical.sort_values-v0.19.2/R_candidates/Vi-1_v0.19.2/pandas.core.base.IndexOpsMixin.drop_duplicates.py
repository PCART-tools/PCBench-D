    @deprecate_kwarg('take_last', 'keep', mapping={True: 'last',
                                                   False: 'first'})
    @Appender(_shared_docs['drop_duplicates'] % _indexops_doc_kwargs)
    def drop_duplicates(self, keep='first', inplace=False):
        if isinstance(self, ABCIndexClass):
            if self.is_unique:
                return self._shallow_copy()

        duplicated = self.duplicated(keep=keep)
        result = self[np.logical_not(duplicated)]
        if inplace:
            return self._update_inplace(result)
        else:
            return result
