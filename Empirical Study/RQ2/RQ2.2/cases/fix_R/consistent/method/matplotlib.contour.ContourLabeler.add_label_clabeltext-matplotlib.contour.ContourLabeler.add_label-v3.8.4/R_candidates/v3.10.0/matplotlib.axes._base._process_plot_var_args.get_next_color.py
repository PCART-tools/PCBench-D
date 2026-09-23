    def get_next_color(self):
        """Return the next color in the cycle."""
        entry = self._cycler_items[self._idx]
        if "color" in entry:
            self._idx = (self._idx + 1) % len(self._cycler_items)  # Advance cycler.
            return entry["color"]
        else:
            return "k"
