    def __init__(self, useOffset=None, useMathText=None, useLocale=None, *,
                 usetex=None):
        if useOffset is None:
            useOffset = mpl.rcParams['axes.formatter.useoffset']
        self._offset_threshold = \
            mpl.rcParams['axes.formatter.offset_threshold']
        self.set_useOffset(useOffset)
        self.set_usetex(usetex)
        self.set_useMathText(useMathText)
        self.orderOfMagnitude = 0
        self.format = ''
        self._scientific = True
        self._powerlimits = mpl.rcParams['axes.formatter.limits']
        self.set_useLocale(useLocale)
