    @Appender(_index_shared_docs["index_unique"] % _index_doc_kwargs)
    def unique(self, level=None):

        if level is None:
            return super().unique()
        else:
            level = self._get_level_number(level)
            return self._get_level_values(level=level, unique=True)
