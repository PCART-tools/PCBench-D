    @size.setter
    def size(self, value):
        if value not in self.info["sizes"]:
            msg = "This is not one of the allowed sizes of this image"
            raise ValueError(msg)
        self._size = value
