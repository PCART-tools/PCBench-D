    def font_variant(
        self, font=None, size=None, index=None, encoding=None, layout_engine=None
    ):
        """
        Create a copy of this FreeTypeFont object,
        using any specified arguments to override the settings.

        Parameters are identical to the parameters used to initialize this
        object.

        :return: A FreeTypeFont object.
        """
        if font is None:
            try:
                font = BytesIO(self.font_bytes)
            except AttributeError:
                font = self.path
        return FreeTypeFont(
            font=font,
            size=self.size if size is None else size,
            index=self.index if index is None else index,
            encoding=self.encoding if encoding is None else encoding,
            layout_engine=layout_engine or self.layout_engine,
        )
