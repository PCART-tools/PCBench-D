    def get_path(self):
        """Return the mutated path of the rectangle."""
        boxstyle = self.get_boxstyle()
        m_aspect = self.get_mutation_aspect()
        # Call boxstyle with y, height squeezed by aspect_ratio.
        path = boxstyle(self._x, self._y / m_aspect,
                        self._width, self._height / m_aspect,
                        self.get_mutation_scale())
        return Path(path.vertices * [1, m_aspect], path.codes)  # Unsqueeze y.
