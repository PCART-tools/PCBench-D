    def update_from(self, other):
        """Copy properties from *other* to *self*."""
        self._transform = other._transform
        self._transformSet = other._transformSet
        self._visible = other._visible
        self._alpha = other._alpha
        self.clipbox = other.clipbox
        self._clipon = other._clipon
        self._clippath = other._clippath
        self._label = other._label
        self._sketch = other._sketch
        self._path_effects = other._path_effects
        self.sticky_edges.x[:] = other.sticky_edges.x.copy()
        self.sticky_edges.y[:] = other.sticky_edges.y.copy()
        self.pchanged()
        self.stale = True
