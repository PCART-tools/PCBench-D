    def __init__(self, s,
                 textprops=None,
                 multilinebaseline=None,
                 minimumdescent=True,
                 ):
        """
        Parameters
        ----------
        s : str
            a string to be displayed.

        textprops : dictionary, optional, default: None
            Dictionary of keyword parameters to be passed to the
            `~matplotlib.text.Text` instance contained inside TextArea.

        multilinebaseline : bool, optional
            If `True`, baseline for multiline text is adjusted so that it is
            (approximately) center-aligned with singleline text.

        minimumdescent : bool, optional
            If `True`, the box has a minimum descent of "p".
        """
        if textprops is None:
            textprops = {}
        textprops.setdefault("va", "baseline")
        self._text = mtext.Text(0, 0, s, **textprops)
        OffsetBox.__init__(self)
        self._children = [self._text]
        self.offset_transform = mtransforms.Affine2D()
        self._baseline_transform = mtransforms.Affine2D()
        self._text.set_transform(self.offset_transform +
                                 self._baseline_transform)
        self._multilinebaseline = multilinebaseline
        self._minimumdescent = minimumdescent
