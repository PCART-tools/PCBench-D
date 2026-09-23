    @size.setter
    def size(self, value: tuple[int, int] | tuple[int, int, int]) -> None:
        if len(value) == 3:
            deprecate("Setting size to (width, height, scale)", 12, "load(scale)")
            if value in self.info["sizes"]:
                self._size = value  # type: ignore[assignment]
                return
        else:
            # Check that a matching size exists,
            # or that there is a scale that would create a size that matches
            for size in self.info["sizes"]:
                simple_size = size[0] * size[2], size[1] * size[2]
                scale = simple_size[0] // value[0]
                if simple_size[1] / value[1] == scale:
                    self._size = value
                    return
        msg = "This is not one of the allowed sizes of this image"
        raise ValueError(msg)
