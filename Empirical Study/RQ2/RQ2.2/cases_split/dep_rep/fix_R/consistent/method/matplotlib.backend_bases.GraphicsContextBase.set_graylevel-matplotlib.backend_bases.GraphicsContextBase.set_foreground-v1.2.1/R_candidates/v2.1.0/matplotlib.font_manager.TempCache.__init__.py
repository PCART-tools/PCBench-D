    def __init__(self):
        self._lookup_cache = {}
        self._last_rcParams = self.make_rcparams_key()
