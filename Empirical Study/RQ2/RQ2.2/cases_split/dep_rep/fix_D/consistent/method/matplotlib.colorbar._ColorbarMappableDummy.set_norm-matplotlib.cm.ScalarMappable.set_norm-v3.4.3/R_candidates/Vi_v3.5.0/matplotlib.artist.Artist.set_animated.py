    def set_animated(self, b):
        """
        Set whether the artist is intended to be used in an animation.

        If True, the artist is excluded from regular drawing of the figure.
        You have to call `.Figure.draw_artist` / `.Axes.draw_artist`
        explicitly on the artist. This appoach is used to speed up animations
        using blitting.

        See also `matplotlib.animation` and
        :doc:`/tutorials/advanced/blitting`.

        Parameters
        ----------
        b : bool
        """
        if self._animated != b:
            self._animated = b
            self.pchanged()
