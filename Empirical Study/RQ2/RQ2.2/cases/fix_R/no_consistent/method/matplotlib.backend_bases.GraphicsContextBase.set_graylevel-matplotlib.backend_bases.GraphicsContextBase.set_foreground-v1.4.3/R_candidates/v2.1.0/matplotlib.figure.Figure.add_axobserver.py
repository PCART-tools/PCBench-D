    def add_axobserver(self, func):
        'whenever the axes state change, ``func(self)`` will be called'
        self._axobservers.append(func)
