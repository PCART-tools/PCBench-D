        def __init__(self, im: Image.Image | str | QByteArray) -> None:
            """
            An PIL image wrapper for Qt.  This is a subclass of PyQt's QImage
            class.

            :param im: A PIL Image object, or a file name (given either as
                Python string or a PyQt string object).
            """
            im_data = _toqclass_helper(im)
            # must keep a reference, or Qt will crash!
            # All QImage constructors that take data operate on an existing
            # buffer, so this buffer has to hang on for the life of the image.
            # Fixes https://github.com/python-pillow/Pillow/issues/1370
            self.__data = im_data["data"]
            super().__init__(
                self.__data,
                im_data["size"][0],
                im_data["size"][1],
                im_data["format"],
            )
            if im_data["colortable"]:
                self.setColorTable(im_data["colortable"])
