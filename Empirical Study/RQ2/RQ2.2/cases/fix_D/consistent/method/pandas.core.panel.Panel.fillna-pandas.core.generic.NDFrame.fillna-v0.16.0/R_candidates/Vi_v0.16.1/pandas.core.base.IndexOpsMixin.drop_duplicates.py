    @Appender(_shared_docs['drop_duplicates'] % _indexops_doc_kwargs)
    def drop_duplicates(self, take_last=False, inplace=False):
        duplicated = self.duplicated(take_last=take_last)
        result = self[np.logical_not(duplicated)]
        if inplace:
            return self._update_inplace(result)
        else:
            return result
