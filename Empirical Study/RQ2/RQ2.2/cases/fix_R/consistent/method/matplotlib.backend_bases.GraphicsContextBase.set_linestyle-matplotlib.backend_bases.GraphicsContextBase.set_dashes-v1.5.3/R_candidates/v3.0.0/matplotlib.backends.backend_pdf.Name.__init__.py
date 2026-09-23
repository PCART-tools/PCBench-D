    def __init__(self, name):
        if isinstance(name, Name):
            self.name = name.name
        else:
            if isinstance(name, bytes):
                name = name.decode('ascii')
            self.name = self._regex.sub(Name.hexify, name).encode('ascii')
