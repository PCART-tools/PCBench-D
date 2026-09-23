    def __init__(
        self,
        size: tuple[int, int],
        kernel: Sequence[float],
        scale: float | None = None,
        offset: float = 0,
    ) -> None:
        if scale is None:
            # default scale is sum of kernel
            scale = functools.reduce(lambda a, b: a + b, kernel)
        if size[0] * size[1] != len(kernel):
            msg = "not enough coefficients in kernel"
            raise ValueError(msg)
        self.filterargs = size, scale, offset, kernel
