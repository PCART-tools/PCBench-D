    def __init__(
        self, image_or_list: Image.Image | list[int], mask: Image.Image | None = None
    ) -> None:
        """
        Calculate statistics for the given image. If a mask is included,
        only the regions covered by that mask are included in the
        statistics. You can also pass in a previously calculated histogram.

        :param image: A PIL image, or a precalculated histogram.

            .. note::

                For a PIL image, calculations rely on the
                :py:meth:`~PIL.Image.Image.histogram` method. The pixel counts are
                grouped into 256 bins, even if the image has more than 8 bits per
                channel. So ``I`` and ``F`` mode images have a maximum ``mean``,
                ``median`` and ``rms`` of 255, and cannot have an ``extrema`` maximum
                of more than 255.

        :param mask: An optional mask.
        """
        if isinstance(image_or_list, Image.Image):
            self.h = image_or_list.histogram(mask)
        elif isinstance(image_or_list, list):
            self.h = image_or_list
        else:
            msg = "first argument must be image or list"  # type: ignore[unreachable]
            raise TypeError(msg)
        self.bands = list(range(len(self.h) // 256))
