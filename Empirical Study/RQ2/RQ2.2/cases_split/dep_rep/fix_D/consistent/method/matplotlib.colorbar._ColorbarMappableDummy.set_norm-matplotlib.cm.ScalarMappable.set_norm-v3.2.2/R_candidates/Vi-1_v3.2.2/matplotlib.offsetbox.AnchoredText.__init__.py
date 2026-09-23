    def __init__(self, s, loc, pad=0.4, borderpad=0.5, prop=None, **kwargs):
        """
        Parameters
        ----------
        s : str
            Text.

        loc : str
            Location code.

        pad : float, optional
            Pad between the text and the frame as fraction of the font
            size.

        borderpad : float, optional
            Pad between the frame and the axes (or *bbox_to_anchor*).

        prop : dictionary, optional, default: None
            Dictionary of keyword parameters to be passed to the
            `~matplotlib.text.Text` instance contained inside AnchoredText.

        Notes
        -----
        Other keyword parameters of `AnchoredOffsetbox` are also
        allowed.
        """

        if prop is None:
            prop = {}
        badkwargs = {'ha', 'horizontalalignment', 'va', 'verticalalignment'}
        if badkwargs & set(prop):
            cbook.warn_deprecated(
                "3.1", message="Mixing horizontalalignment or "
                "verticalalignment with AnchoredText is not supported, "
                "deprecated since %(since)s, and will raise an exception "
                "%(removal)s.")

        self.txt = TextArea(s, textprops=prop, minimumdescent=False)
        fp = self.txt._text.get_fontproperties()
        super().__init__(
            loc, pad=pad, borderpad=borderpad, child=self.txt, prop=fp,
            **kwargs)
