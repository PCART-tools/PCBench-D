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

        textprops : `~matplotlib.font_manager.FontProperties`, optional

        multilinebaseline : bool, optional
            If `True`, baseline for multiline text is adjusted so that
            it is (approximatedly) center-aligned with singleline
            text.

        minimumdescent : bool, optional
            If `True`, the box has a minimum descent of "p".
        """
        if textprops is None:
            textprops = {}

        if "va" not in textprops:
            textprops["va"] = "baseline"

        self._text = mtext.Text(0, 0, s, **textprops)

        OffsetBox.__init__(self)

        self._children = [self._text]

        self.offset_transform = mtransforms.Affine2D()
        self.offset_transform.clear()
        self.offset_transform.translate(0, 0)
        self._baseline_transform = mtransforms.Affine2D()
        self._text.set_transform(self.offset_transform +
                                 self._baseline_transform)

        self._multilinebaseline = multilinebaseline
        self._minimumdescent = minimumdescent
