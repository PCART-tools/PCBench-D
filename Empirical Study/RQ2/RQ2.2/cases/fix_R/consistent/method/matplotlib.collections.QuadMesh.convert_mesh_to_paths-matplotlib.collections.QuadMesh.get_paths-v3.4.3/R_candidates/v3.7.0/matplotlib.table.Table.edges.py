    @edges.setter
    def edges(self, value):
        self._edges = value
        self.stale = True
