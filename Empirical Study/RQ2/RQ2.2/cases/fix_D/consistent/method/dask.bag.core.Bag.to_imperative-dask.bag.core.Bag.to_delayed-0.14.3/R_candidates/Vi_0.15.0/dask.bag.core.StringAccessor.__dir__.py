    def __dir__(self):
        return sorted(set(dir(type(self)) + dir(str)))
