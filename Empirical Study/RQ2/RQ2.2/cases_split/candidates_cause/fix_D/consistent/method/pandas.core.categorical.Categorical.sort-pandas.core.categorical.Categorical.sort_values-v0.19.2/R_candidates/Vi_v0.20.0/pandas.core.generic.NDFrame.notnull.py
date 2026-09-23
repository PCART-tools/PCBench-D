    @Appender(_shared_docs['isnotnull'])
    def notnull(self):
        return notnull(self).__finalize__(self)
