    def __init__(self, init=()):
        mapping = self._mapping = {}
        for x in init:
            mapping[ref(x)] = [ref(x)]
