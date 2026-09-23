    def get_variation_names(self) -> list[bytes]:
        """
        :returns: A list of the named styles in a variation font.
        :exception OSError: If the font is not a variation font.
        """
        try:
            names = self.font.getvarnames()
        except AttributeError as e:
            msg = "FreeType 2.9.1 or greater is required"
            raise NotImplementedError(msg) from e
        return [name.replace(b"\x00", b"") for name in names]
