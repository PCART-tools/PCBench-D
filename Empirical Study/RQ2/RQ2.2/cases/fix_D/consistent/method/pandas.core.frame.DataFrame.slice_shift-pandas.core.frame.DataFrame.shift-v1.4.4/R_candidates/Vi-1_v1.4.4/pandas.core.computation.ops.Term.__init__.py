    def __init__(self, name, env, side=None, encoding=None):
        # name is a str for Term, but may be something else for subclasses
        self._name = name
        self.env = env
        self.side = side
        tname = str(name)
        self.is_local = tname.startswith(LOCAL_TAG) or tname in DEFAULT_GLOBALS
        self._value = self._resolve_name()
        self.encoding = encoding
