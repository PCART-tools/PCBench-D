    @visible_edges.setter
    def visible_edges(self, value):
        if value is None:
            self._visible_edges = self._edges
        elif value in self._edge_aliases:
            self._visible_edges = self._edge_aliases[value]
        else:
            for edge in value:
                if edge not in self._edges:
                    msg = ('Invalid edge param {0}, must only be one of'
                           ' {1} or string of {2}.').format(
                                   value,
                                   ", ".join(self._edge_aliases),
                                   ", ".join(self._edges),
                                   )
                    raise ValueError(msg)
            self._visible_edges = value
        self.stale = True
