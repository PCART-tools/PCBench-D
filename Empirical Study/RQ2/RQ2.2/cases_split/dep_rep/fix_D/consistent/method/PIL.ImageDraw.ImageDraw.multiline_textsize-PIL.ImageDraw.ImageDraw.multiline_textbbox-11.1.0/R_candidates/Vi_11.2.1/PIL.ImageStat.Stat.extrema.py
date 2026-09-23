    @cached_property
    def extrema(self) -> list[tuple[int, int]]:
        """
        Min/max values for each band in the image.

        .. note::
            This relies on the :py:meth:`~PIL.Image.Image.histogram` method, and
            simply returns the low and high bins used. This is correct for
            images with 8 bits per channel, but fails for other modes such as
            ``I`` or ``F``. Instead, use :py:meth:`~PIL.Image.Image.getextrema` to
            return per-band extrema for the image. This is more correct and
            efficient because, for non-8-bit modes, the histogram method uses
            :py:meth:`~PIL.Image.Image.getextrema` to determine the bins used.
        """

        def minmax(histogram: list[int]) -> tuple[int, int]:
            res_min, res_max = 255, 0
            for i in range(256):
                if histogram[i]:
                    res_min = i
                    break
            for i in range(255, -1, -1):
                if histogram[i]:
                    res_max = i
                    break
            return res_min, res_max

        return [minmax(self.h[i:]) for i in range(0, len(self.h), 256)]
