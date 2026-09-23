    def sizes(self):
        """
        Get a list of all available icon sizes and color depths.
        """
        return {(h["width"], h["height"]) for h in self.entry}
