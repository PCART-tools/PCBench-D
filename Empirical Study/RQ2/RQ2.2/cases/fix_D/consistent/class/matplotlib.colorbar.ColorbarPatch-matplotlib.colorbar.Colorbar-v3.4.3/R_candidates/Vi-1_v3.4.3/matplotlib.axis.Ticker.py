class Ticker:
    """
    A container for the objects defining tick position and format.

    Attributes
    ----------
    locator : `matplotlib.ticker.Locator` subclass
        Determines the positions of the ticks.
    formatter : `matplotlib.ticker.Formatter` subclass
        Determines the format of the tick labels.
    """

    def __init__(self):
        self._locator = None
        self._formatter = None

    @property
    def locator(self):
        return self._locator

    @locator.setter
    def locator(self, locator):
        if not isinstance(locator, mticker.Locator):
            raise TypeError('locator must be a subclass of '
                            'matplotlib.ticker.Locator')
        self._locator = locator

    @property
    def formatter(self):
        return self._formatter

    @formatter.setter
    def formatter(self, formatter):
        if not isinstance(formatter, mticker.Formatter):
            raise TypeError('formatter must be a subclass of '
                            'matplotlib.ticker.Formatter')
        self._formatter = formatter
