    def get_next_color(self):
        """Return the next color in the cycle."""
        if 'color' not in self._prop_keys:
            return 'k'
        c = self._cycler_items[self._idx]['color']
        self._idx = (self._idx + 1) % len(self._cycler_items)
        return c
