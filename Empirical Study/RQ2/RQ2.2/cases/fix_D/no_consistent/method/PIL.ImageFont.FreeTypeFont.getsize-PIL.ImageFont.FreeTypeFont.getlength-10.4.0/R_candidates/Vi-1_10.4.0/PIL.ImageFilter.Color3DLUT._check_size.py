    @staticmethod
    def _check_size(size: Any) -> tuple[int, int, int]:
        try:
            _, _, _ = size
        except ValueError as e:
            msg = "Size should be either an integer or a tuple of three integers."
            raise ValueError(msg) from e
        except TypeError:
            size = (size, size, size)
        size = tuple(int(x) for x in size)
        for size_1d in size:
            if not 2 <= size_1d <= 65:
                msg = "Size should be in [2, 65] range."
                raise ValueError(msg)
        return size
