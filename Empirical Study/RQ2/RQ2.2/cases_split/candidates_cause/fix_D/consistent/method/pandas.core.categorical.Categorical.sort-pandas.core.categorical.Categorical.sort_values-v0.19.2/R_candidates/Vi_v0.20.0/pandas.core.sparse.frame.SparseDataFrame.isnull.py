    @Appender(generic._shared_docs['isnull'])
    def isnull(self):
        return self._apply_columns(lambda x: x.isnull())
