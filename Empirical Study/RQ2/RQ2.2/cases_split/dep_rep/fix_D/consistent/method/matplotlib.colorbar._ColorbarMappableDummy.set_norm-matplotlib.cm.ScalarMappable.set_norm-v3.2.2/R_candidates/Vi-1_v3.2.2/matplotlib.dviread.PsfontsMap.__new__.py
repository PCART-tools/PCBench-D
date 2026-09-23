    @lru_cache()
    def __new__(cls, filename):
        self = object.__new__(cls)
        self._font = {}
        self._filename = os.fsdecode(filename)
        with open(filename, 'rb') as file:
            self._parse(file)
        return self
