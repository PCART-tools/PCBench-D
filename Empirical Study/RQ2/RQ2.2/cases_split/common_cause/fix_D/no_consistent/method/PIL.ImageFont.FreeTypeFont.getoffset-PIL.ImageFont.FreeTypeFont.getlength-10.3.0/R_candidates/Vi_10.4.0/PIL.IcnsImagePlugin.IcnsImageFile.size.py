    @size.setter
    def size(self, value):
        info_size = value
        if info_size not in self.info["sizes"] and len(info_size) == 2:
            info_size = (info_size[0], info_size[1], 1)
        if (
            info_size not in self.info["sizes"]
            and len(info_size) == 3
            and info_size[2] == 1
        ):
            simple_sizes = [
                (size[0] * size[2], size[1] * size[2]) for size in self.info["sizes"]
            ]
            if value in simple_sizes:
                info_size = self.info["sizes"][simple_sizes.index(value)]
        if info_size not in self.info["sizes"]:
            msg = "This is not one of the allowed sizes of this image"
            raise ValueError(msg)
        self._size = value
