    @Appender(_index_shared_docs['__contains__'] % _index_doc_kwargs)
    def __contains__(self, key):
        hash(key)
        try:
            self.get_loc(key)
            return True
        except LookupError:
            return False
