    @Appender(_shared_docs['isnull'])
    def isnull(self):
        return isnull(self).__finalize__(self)
