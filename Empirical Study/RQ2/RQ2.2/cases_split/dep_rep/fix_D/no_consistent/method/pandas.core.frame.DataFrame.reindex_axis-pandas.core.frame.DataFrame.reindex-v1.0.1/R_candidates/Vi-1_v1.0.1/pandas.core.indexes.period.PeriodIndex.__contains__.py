    @Appender(_index_shared_docs["contains"])
    def __contains__(self, key) -> bool:
        if isinstance(key, Period):
            if key.freq != self.freq:
                return False
            else:
                return key.ordinal in self._engine
        else:
            try:
                self.get_loc(key)
                return True
            except (TypeError, KeyError):
                # TypeError can be reached if we pass a tuple that is not hashable
                return False
