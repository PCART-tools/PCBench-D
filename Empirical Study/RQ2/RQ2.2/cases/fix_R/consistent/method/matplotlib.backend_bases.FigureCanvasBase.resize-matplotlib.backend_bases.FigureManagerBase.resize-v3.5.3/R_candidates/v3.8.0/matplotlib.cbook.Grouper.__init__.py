    def __init__(self, init=()):
        self._mapping = weakref.WeakKeyDictionary(
            {x: weakref.WeakSet([x]) for x in init})
