    @property
    def _axis_map(self):
        """A mapping of axis names, e.g. 'x', to `Axis` instances."""
        return {name: getattr(self, f"{name}axis")
                for name in self._axis_names}
