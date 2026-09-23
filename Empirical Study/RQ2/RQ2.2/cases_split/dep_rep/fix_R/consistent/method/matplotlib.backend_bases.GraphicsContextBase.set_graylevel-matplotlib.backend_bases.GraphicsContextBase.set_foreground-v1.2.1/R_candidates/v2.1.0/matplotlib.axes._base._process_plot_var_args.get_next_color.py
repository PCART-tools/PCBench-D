    def get_next_color(self):
        """
        Return the next color in the cycle.
        """
        if 'color' not in self._prop_keys:
            return 'k'
        return six.next(self.prop_cycler)['color']
