    def sizes(self) -> set[tuple[int, int]]:
        """
        Get a set of all available icon sizes and color depths.
        """
        return {(h.width, h.height) for h in self.entry}
