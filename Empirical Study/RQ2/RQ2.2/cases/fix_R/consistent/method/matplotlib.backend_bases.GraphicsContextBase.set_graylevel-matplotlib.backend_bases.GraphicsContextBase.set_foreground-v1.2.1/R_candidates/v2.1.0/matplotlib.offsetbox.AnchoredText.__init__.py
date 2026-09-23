    def __init__(self, s, loc, pad=0.4, borderpad=0.5, prop=None, **kwargs):
        """
        Parameters
        ----------
        s : string
            Text.

        loc : str
            Location code.

        pad : float, optional
            Pad between the text and the frame as fraction of the font
            size.

        borderpad : float, optional
            Pad between the frame and the axes (or *bbox_to_anchor*).

        prop : `matplotlib.font_manager.FontProperties`
            Font properties.

        Notes
        -----
        Other keyword parameters of `AnchoredOffsetbox` are also
        allowed.
        """

        if prop is None:
            prop = {}
        badkwargs = {'ha', 'horizontalalignment', 'va', 'verticalalignment'}
        if badkwargs & set(prop):
            warnings.warn("Mixing horizontalalignment or verticalalignment "
                          "with AnchoredText is not supported.")

        self.txt = TextArea(s, textprops=prop, minimumdescent=False)
        fp = self.txt._text.get_fontproperties()
        super(AnchoredText, self).__init__(
            loc, pad=pad, borderpad=borderpad, child=self.txt, prop=fp,
            **kwargs)
