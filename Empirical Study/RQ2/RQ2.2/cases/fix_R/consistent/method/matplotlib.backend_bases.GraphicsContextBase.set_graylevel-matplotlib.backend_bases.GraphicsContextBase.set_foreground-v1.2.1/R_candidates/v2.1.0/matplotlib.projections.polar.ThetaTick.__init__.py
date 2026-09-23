    def __init__(self, axes, *args, **kwargs):
        self._text1_translate = mtransforms.ScaledTranslation(
            0, 0,
            axes.figure.dpi_scale_trans)
        self._text2_translate = mtransforms.ScaledTranslation(
            0, 0,
            axes.figure.dpi_scale_trans)
        super(ThetaTick, self).__init__(axes, *args, **kwargs)
