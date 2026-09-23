    def apply(self, image: Image.Image) -> tuple[int, Image.Image]:
        """Run a single morphological operation on an image

        Returns a tuple of the number of changed pixels and the
        morphed image"""
        if self.lut is None:
            msg = "No operator loaded"
            raise Exception(msg)

        if image.mode != "L":
            msg = "Image mode must be L"
            raise ValueError(msg)
        outimage = Image.new(image.mode, image.size, None)
        count = _imagingmorph.apply(bytes(self.lut), image.getim(), outimage.getim())
        return count, outimage
