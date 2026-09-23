    def crop(self, box=None):
        """
        Returns a rectangular region from this image. The box is a
        4-tuple defining the left, upper, right, and lower pixel
        coordinate. See :ref:`coordinate-system`.

        Note: Prior to Pillow 3.4.0, this was a lazy operation.

        :param box: The crop rectangle, as a (left, upper, right, lower)-tuple.
        :rtype: :py:class:`~PIL.Image.Image`
        :returns: An :py:class:`~PIL.Image.Image` object.
        """

        if box is None:
            return self.copy()

        if box[2] < box[0]:
            msg = "Coordinate 'right' is less than 'left'"
            raise ValueError(msg)
        elif box[3] < box[1]:
            msg = "Coordinate 'lower' is less than 'upper'"
            raise ValueError(msg)

        self.load()
        return self._new(self._crop(self.im, box))
