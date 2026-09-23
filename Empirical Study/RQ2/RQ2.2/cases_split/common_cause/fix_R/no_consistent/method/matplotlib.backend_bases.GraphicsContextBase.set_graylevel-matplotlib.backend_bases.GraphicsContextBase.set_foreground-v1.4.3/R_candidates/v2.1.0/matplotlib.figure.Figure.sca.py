    def sca(self, a):
        'Set the current axes to be a and return a'
        self._axstack.bubble(a)
        for func in self._axobservers:
            func(self)
        return a
