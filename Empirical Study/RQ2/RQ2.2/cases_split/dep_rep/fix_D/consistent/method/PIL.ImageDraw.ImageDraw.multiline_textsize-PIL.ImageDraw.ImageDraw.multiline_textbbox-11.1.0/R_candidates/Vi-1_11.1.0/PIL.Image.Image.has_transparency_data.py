    @property
    def has_transparency_data(self) -> bool:
        """
        Determine if an image has transparency data, whether in the form of an
        alpha channel, a palette with an alpha channel, or a "transparency" key
        in the info dictionary.

        Note the image might still appear solid, if all of the values shown
        within are opaque.

        :returns: A boolean.
        """
        if (
            self.mode in ("LA", "La", "PA", "RGBA", "RGBa")
            or "transparency" in self.info
        ):
            return True
        if self.mode == "P":
            assert self.palette is not None
            return self.palette.mode.endswith("A")
        return False
