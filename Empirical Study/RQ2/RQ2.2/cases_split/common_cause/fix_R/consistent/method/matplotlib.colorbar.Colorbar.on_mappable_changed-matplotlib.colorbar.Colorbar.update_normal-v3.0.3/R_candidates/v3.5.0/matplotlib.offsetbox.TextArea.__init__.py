    @_api.delete_parameter("3.4", "minimumdescent")
    def __init__(self, s,
                 textprops=None,
                 multilinebaseline=False,
                 minimumdescent=True,
                 ):
        """
        Parameters
        ----------
        s : str
            The text to be displayed.
        textprops : dict, default: {}
            Dictionary of keyword parameters to be passed to the `.Text`
            instance in the TextArea.
        multilinebaseline : bool, default: False
            Whether the baseline for multiline text is adjusted so that it
            is (approximately) center-aligned with single-line text.
        minimumdescent : bool, default: True
            If `True`, the box has a minimum descent of "p".  This is now
            effectively always True.
        """
        if textprops is None:
            textprops = {}
        self._text = mtext.Text(0, 0, s, **textprops)
        super().__init__()
        self._children = [self._text]
        self.offset_transform = mtransforms.Affine2D()
        self._baseline_transform = mtransforms.Affine2D()
        self._text.set_transform(self.offset_transform +
                                 self._baseline_transform)
        self._multilinebaseline = multilinebaseline
        self._minimumdescent = minimumdescent
