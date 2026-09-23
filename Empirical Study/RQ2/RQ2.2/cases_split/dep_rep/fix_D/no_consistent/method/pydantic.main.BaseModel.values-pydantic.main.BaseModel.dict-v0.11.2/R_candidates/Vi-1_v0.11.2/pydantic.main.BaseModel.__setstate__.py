    def __setstate__(self, state):
        object.__setattr__(self, '__values__', state)
