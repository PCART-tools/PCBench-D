    @Appender(_index_shared_docs['__contains__'] % _index_doc_kwargs)
    def __contains__(self, key):
        try:
            res = self.get_loc(key)
            return is_scalar(res) or type(res) == slice or np.any(res)
        except (KeyError, TypeError, ValueError):
            return False
