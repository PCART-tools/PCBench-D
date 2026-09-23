    def get_autoscale_on(self):
        """Return True if each axis is autoscaled, False otherwise."""
        return all(axis._get_autoscale_on()
                   for axis in self._axis_map.values())
