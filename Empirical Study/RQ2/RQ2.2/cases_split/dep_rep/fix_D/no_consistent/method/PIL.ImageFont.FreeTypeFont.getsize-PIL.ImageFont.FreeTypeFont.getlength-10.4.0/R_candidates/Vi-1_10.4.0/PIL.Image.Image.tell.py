    def tell(self) -> int:
        """
        Returns the current frame number. See :py:meth:`~PIL.Image.Image.seek`.

        If defined, :attr:`~PIL.Image.Image.n_frames` refers to the
        number of available frames.

        :returns: Frame number, starting with 0.
        """
        return 0
