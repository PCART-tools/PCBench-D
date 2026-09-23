    def set_caption(self, caption: str | tuple | list) -> Styler:
        """
        Set the text added to a ``<caption>`` HTML element.

        Parameters
        ----------
        caption : str, tuple, list
            For HTML output either the string input is used or the first element of the
            tuple. For LaTeX the string input provides a caption and the additional
            tuple input allows for full captions and short captions, in that order.

        Returns
        -------
        Styler
        """
        msg = "`caption` must be either a string or 2-tuple of strings."
        if isinstance(caption, (list, tuple)):
            if (
                len(caption) != 2
                or not isinstance(caption[0], str)
                or not isinstance(caption[1], str)
            ):
                raise ValueError(msg)
        elif not isinstance(caption, str):
            raise ValueError(msg)
        self.caption = caption
        return self
