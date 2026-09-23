    def delaxes(self, a):
        'remove a from the figure and update the current axes'
        self._axstack.remove(a)
        for func in self._axobservers:
            func(self)
        self.stale = True
