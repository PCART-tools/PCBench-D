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
        return (
            self.mode in ("LA", "La", "PA", "RGBA", "RGBa")
            or (self.mode == "P" and self.palette.mode.endswith("A"))
            or "transparency" in self.info
        )
