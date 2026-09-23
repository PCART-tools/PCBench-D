    def transpose(self, method):
        """
        Transpose image (flip or rotate in 90 degree steps)

        :param method: One of :py:data:`Transpose.FLIP_LEFT_RIGHT`,
          :py:data:`Transpose.FLIP_TOP_BOTTOM`, :py:data:`Transpose.ROTATE_90`,
          :py:data:`Transpose.ROTATE_180`, :py:data:`Transpose.ROTATE_270`,
          :py:data:`Transpose.TRANSPOSE` or :py:data:`Transpose.TRANSVERSE`.
        :returns: Returns a flipped or rotated copy of this image.
        """

        self.load()
        return self._new(self.im.transpose(method))
