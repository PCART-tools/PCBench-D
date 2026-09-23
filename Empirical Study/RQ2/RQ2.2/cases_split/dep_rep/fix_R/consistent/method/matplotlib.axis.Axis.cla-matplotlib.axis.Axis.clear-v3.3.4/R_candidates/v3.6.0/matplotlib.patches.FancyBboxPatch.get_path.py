    def get_path(self):
        """Return the mutated path of the rectangle."""
        boxstyle = self.get_boxstyle()
        x = self._x
        y = self._y
        width = self._width
        height = self._height
        m_scale = self.get_mutation_scale()
        m_aspect = self.get_mutation_aspect()
        # Squeeze the given height by the aspect_ratio.
        y, height = y / m_aspect, height / m_aspect
        # Call boxstyle with squeezed height.
        try:
            inspect.signature(boxstyle).bind(x, y, width, height, m_scale)
        except TypeError:
            # Don't apply aspect twice.
            path = boxstyle(x, y, width, height, m_scale, 1)
            _api.warn_deprecated(
                "3.4", message="boxstyles must be callable without the "
                "'mutation_aspect' parameter since %(since)s; support for the "
                "old call signature will be removed %(removal)s.")
        else:
            path = boxstyle(x, y, width, height, m_scale)
        vertices, codes = path.vertices, path.codes
        # Restore the height.
        vertices[:, 1] = vertices[:, 1] * m_aspect
        return Path(vertices, codes)
