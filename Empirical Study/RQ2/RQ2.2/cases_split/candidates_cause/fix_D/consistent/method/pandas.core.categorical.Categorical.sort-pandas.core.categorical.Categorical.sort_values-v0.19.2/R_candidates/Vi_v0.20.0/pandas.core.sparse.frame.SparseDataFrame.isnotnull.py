    @Appender(generic._shared_docs['isnotnull'])
    def isnotnull(self):
        return self._apply_columns(lambda x: x.isnotnull())
