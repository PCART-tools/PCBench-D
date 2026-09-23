    @Appender(_index_shared_docs["contains"] % _index_doc_kwargs)
    def __contains__(self, key) -> bool:
        hash(key)
        try:
            self.get_loc(key)
            return True
        except (LookupError, TypeError, ValueError):
            return False
