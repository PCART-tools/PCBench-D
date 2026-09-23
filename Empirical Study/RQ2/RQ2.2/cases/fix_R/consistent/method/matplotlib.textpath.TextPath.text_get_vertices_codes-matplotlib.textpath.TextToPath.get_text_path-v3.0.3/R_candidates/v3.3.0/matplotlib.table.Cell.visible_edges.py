    @visible_edges.setter
    def visible_edges(self, value):
        if value is None:
            self._visible_edges = self._edges
        elif value in self._edge_aliases:
            self._visible_edges = self._edge_aliases[value]
        else:
            if any(edge not in self._edges for edge in value):
                raise ValueError('Invalid edge param {}, must only be one of '
                                 '{} or string of {}'.format(
                                     value,
                                     ", ".join(self._edge_aliases),
                                     ", ".join(self._edges)))
            self._visible_edges = value
        self.stale = True
