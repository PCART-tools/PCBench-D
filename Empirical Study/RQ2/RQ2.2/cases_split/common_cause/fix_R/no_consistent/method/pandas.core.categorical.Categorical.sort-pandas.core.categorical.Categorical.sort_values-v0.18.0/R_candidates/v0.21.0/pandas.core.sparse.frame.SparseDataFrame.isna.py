    @Appender(generic._shared_docs['isna'])
    def isna(self):
        return self._apply_columns(lambda x: x.isna())
