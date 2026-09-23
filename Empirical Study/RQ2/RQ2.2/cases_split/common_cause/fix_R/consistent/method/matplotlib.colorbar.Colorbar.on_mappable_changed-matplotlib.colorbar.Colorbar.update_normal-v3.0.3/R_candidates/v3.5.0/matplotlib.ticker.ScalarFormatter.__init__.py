    def __init__(self, useOffset=None, useMathText=None, useLocale=None):
        if useOffset is None:
            useOffset = mpl.rcParams['axes.formatter.useoffset']
        self._offset_threshold = \
            mpl.rcParams['axes.formatter.offset_threshold']
        self.set_useOffset(useOffset)
        self._usetex = mpl.rcParams['text.usetex']
        if useMathText is None:
            useMathText = mpl.rcParams['axes.formatter.use_mathtext']
            if useMathText is False:
                try:
                    ufont = mpl.font_manager.findfont(
                        mpl.font_manager.FontProperties(
                            mpl.rcParams["font.family"]
                        ),
                        fallback_to_default=False,
                    )
                except ValueError:
                    ufont = None

                if ufont == str(cbook._get_data_path("fonts/ttf/cmr10.ttf")):
                    _api.warn_external(
                        "cmr10 font should ideally be used with "
                        "mathtext, set axes.formatter.use_mathtext to True"
                    )
        self.set_useMathText(useMathText)
        self.orderOfMagnitude = 0
        self.format = ''
        self._scientific = True
        self._powerlimits = mpl.rcParams['axes.formatter.limits']
        if useLocale is None:
            useLocale = mpl.rcParams['axes.formatter.use_locale']
        self._useLocale = useLocale
