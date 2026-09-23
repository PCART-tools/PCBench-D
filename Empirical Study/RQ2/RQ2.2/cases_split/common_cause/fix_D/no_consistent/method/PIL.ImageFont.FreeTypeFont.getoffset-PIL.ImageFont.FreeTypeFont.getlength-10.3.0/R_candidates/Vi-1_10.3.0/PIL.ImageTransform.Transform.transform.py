    def transform(
        self,
        size: tuple[int, int],
        image: Image.Image,
        **options: dict[str, str | int | tuple[int, ...] | list[int]],
    ) -> Image.Image:
        """Perform the transform. Called from :py:meth:`.Image.transform`."""
        # can be overridden
        method, data = self.getdata()
        return image.transform(size, method, data, **options)
