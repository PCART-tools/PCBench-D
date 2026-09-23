    def paste(self, im: Image.Image) -> None:
        """
        Paste a PIL image into the photo image.  Note that this can
        be very slow if the photo image is displayed.

        :param im: A PIL image. The size must match the target region.  If the
                   mode does not match, the image is converted to the mode of
                   the bitmap image.
        """
        # convert to blittable
        ptr = im.getim()
        image = im.im
        if not image.isblock() or im.mode != self.__mode:
            block = Image.core.new_block(self.__mode, im.size)
            image.convert2(block, image)  # convert directly between buffers
            ptr = block.ptr

        _pyimagingtkcall("PyImagingPhoto", self.__photo, ptr)
