    @doc(Index.__contains__)
    def __contains__(self, key: Any) -> bool:
        if isinstance(key, Period):
            if key.freq != self.freq:
                return False
            else:
                return key.ordinal in self._engine
        else:
            hash(key)
            try:
                self.get_loc(key)
                return True
            except KeyError:
                return False
