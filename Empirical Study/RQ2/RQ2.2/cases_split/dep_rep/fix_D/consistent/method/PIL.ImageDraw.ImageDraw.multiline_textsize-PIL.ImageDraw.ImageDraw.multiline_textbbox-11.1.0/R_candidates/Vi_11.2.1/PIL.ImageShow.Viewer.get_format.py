    def get_format(self, image: Image.Image) -> str | None:
        """Return format name, or ``None`` to save as PGM/PPM."""
        return self.format
