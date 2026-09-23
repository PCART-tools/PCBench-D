    @Appender(
        _shared_docs["valid_index"] % {"position": "last", "klass": "Series/DataFrame"}
    )
    def last_valid_index(self):
        return self._find_valid_index("last")
