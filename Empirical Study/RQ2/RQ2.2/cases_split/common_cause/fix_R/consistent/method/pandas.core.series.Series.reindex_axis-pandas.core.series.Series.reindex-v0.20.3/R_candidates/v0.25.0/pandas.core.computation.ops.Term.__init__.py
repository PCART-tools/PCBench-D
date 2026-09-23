    def __init__(self, name, env, side=None, encoding=None):
        self._name = name
        self.env = env
        self.side = side
        tname = str(name)
        self.is_local = tname.startswith(_LOCAL_TAG) or tname in _DEFAULT_GLOBALS
        self._value = self._resolve_name()
        self.encoding = encoding
