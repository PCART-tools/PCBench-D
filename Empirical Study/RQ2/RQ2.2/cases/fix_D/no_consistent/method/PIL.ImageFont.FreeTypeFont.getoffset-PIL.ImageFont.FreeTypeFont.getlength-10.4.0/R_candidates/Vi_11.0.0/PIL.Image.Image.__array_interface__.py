    @property
    def __array_interface__(self) -> dict[str, str | bytes | int | tuple[int, ...]]:
        # numpy array interface support
        new: dict[str, str | bytes | int | tuple[int, ...]] = {"version": 3}
        if self.mode == "1":
            # Binary images need to be extended from bits to bytes
            # See: https://github.com/python-pillow/Pillow/issues/350
            new["data"] = self.tobytes("raw", "L")
        else:
            new["data"] = self.tobytes()
        new["shape"], new["typestr"] = _conv_type_shape(self)
        return new
