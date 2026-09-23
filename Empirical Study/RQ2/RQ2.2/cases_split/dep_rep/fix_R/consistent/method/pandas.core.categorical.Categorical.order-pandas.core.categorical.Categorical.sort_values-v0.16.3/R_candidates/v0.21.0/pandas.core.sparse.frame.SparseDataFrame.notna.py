    @Appender(generic._shared_docs['notna'])
    def notna(self):
        return self._apply_columns(lambda x: x.notna())
