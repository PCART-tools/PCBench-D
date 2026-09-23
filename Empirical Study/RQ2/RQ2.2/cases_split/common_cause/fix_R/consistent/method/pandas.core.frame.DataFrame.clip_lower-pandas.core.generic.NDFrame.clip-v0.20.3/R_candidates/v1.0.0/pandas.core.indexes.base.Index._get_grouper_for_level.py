    @Appender(_index_shared_docs["_get_grouper_for_level"])
    def _get_grouper_for_level(self, mapper, level=None):
        assert level is None or level == 0
        if mapper is None:
            grouper = self
        else:
            grouper = self.map(mapper)

        return grouper, None, None
