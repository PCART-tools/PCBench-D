    @property
    def __array_interface__(self):
        # numpy array interface support
        new = {"version": 3}
        try:
            if self.mode == "1":
                # Binary images need to be extended from bits to bytes
                # See: https://github.com/python-pillow/Pillow/issues/350
                new["data"] = self.tobytes("raw", "L")
            else:
                new["data"] = self.tobytes()
        except Exception as e:
            if not isinstance(e, (MemoryError, RecursionError)):
                try:
                    import numpy
                    from packaging.version import parse as parse_version
                except ImportError:
                    pass
                else:
                    if parse_version(numpy.__version__) < parse_version("1.23"):
                        warnings.warn(e)
            raise
        new["shape"], new["typestr"] = _conv_type_shape(self)
        return new
