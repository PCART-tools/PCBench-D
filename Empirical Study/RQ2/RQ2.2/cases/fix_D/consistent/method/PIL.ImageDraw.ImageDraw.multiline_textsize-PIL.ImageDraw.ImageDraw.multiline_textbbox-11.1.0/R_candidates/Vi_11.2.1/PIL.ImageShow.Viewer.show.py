    def show(self, image: Image.Image, **options: Any) -> int:
        """
        The main function for displaying an image.
        Converts the given image to the target format and displays it.
        """

        if not (
            image.mode in ("1", "RGBA")
            or (self.format == "PNG" and image.mode in ("I;16", "LA"))
        ):
            base = Image.getmodebase(image.mode)
            if image.mode != base:
                image = image.convert(base)

        return self.show_image(image, **options)
