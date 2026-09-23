    def _get_layout_cache_key(self, renderer=None):
        """
        Return a hashable tuple of properties that lets `_get_layout` know
        whether a previously computed layout can be reused.
        """
        x, y = self.get_unitless_position()
        renderer = renderer or self._renderer
        return (
            x, y, self.get_text(), hash(self._fontproperties),
            self._verticalalignment, self._horizontalalignment,
            self._linespacing,
            self._rotation, self._rotation_mode, self._transform_rotates_text,
            self.figure.dpi, weakref.ref(renderer),
        )
