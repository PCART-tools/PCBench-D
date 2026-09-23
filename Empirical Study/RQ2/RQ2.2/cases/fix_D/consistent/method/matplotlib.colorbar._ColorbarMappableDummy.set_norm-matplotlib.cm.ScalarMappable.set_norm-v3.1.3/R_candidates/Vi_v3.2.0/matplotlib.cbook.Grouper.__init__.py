    def __init__(self, init=()):
        self._mapping = {weakref.ref(x): [weakref.ref(x)] for x in init}
