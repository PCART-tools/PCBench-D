    def __init__(self, useOffset=None, useMathText=None, useLocale=None):
        # useOffset allows plotting small data ranges with large offsets: for
        # example: [1+1e-9,1+2e-9,1+3e-9] useMathText will render the offset
        # and scientific notation in mathtext

        if useOffset is None:
            useOffset = rcParams['axes.formatter.useoffset']
        self._offset_threshold = rcParams['axes.formatter.offset_threshold']
        self.set_useOffset(useOffset)
        self._usetex = rcParams['text.usetex']
        if useMathText is None:
            useMathText = rcParams['axes.formatter.use_mathtext']
        self.set_useMathText(useMathText)
        self.orderOfMagnitude = 0
        self.format = ''
        self._scientific = True
        self._powerlimits = rcParams['axes.formatter.limits']
        if useLocale is None:
            useLocale = rcParams['axes.formatter.use_locale']
        self._useLocale = useLocale
