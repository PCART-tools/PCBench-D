    def seek(self, frame: int) -> None:
        """
        Seeks to the given frame in this sequence file. If you seek
        beyond the end of the sequence, the method raises an
        ``EOFError`` exception. When a sequence file is opened, the
        library automatically seeks to frame 0.

        See :py:meth:`~PIL.Image.Image.tell`.

        If defined, :attr:`~PIL.Image.Image.n_frames` refers to the
        number of available frames.

        :param frame: Frame number, starting at 0.
        :exception EOFError: If the call attempts to seek beyond the end
            of the sequence.
        """

        # overridden by file handlers
        if frame != 0:
            msg = "no more images in file"
            raise EOFError(msg)
