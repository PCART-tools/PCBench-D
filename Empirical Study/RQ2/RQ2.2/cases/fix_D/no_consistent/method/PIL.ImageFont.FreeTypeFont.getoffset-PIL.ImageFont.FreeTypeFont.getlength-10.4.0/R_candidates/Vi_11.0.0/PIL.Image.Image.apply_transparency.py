    def apply_transparency(self) -> None:
        """
        If a P mode image has a "transparency" key in the info dictionary,
        remove the key and instead apply the transparency to the palette.
        Otherwise, the image is unchanged.
        """
        if self.mode != "P" or "transparency" not in self.info:
            return

        from . import ImagePalette

        palette = self.getpalette("RGBA")
        assert palette is not None
        transparency = self.info["transparency"]
        if isinstance(transparency, bytes):
            for i, alpha in enumerate(transparency):
                palette[i * 4 + 3] = alpha
        else:
            palette[transparency * 4 + 3] = 0
        self.palette = ImagePalette.ImagePalette("RGBA", bytes(palette))
        self.palette.dirty = 1

        del self.info["transparency"]
