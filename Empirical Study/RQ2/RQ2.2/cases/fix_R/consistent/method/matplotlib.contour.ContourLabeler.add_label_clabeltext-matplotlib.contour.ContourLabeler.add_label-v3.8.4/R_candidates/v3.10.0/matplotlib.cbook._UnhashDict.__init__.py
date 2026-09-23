    def __init__(self, pairs):
        self._dict = {}
        self._pairs = []
        for k, v in pairs:
            self[k] = v
