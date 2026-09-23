class AutoDateFormatter(ticker.Formatter):
    """
    A `.Formatter` which attempts to figure out the best format to use.  This
    is most useful when used with the `AutoDateLocator`.

    The AutoDateFormatter has a scale dictionary that maps the scale
    of the tick (the distance in days between one major tick) and a
    format string.  The default looks like this::

        self.scaled = {
            DAYS_PER_YEAR: rcParams['date.autoformat.year'],
            DAYS_PER_MONTH: rcParams['date.autoformat.month'],
            1.0: rcParams['date.autoformat.day'],
            1. / HOURS_PER_DAY: rcParams['date.autoformat.hour'],
            1. / (MINUTES_PER_DAY): rcParams['date.autoformat.minute'],
            1. / (SEC_PER_DAY): rcParams['date.autoformat.second'],
            1. / (MUSECONDS_PER_DAY): rcParams['date.autoformat.microsecond'],
        }

    The algorithm picks the key in the dictionary that is >= the
    current scale and uses that format string.  You can customize this
    dictionary by doing::

    >>> locator = AutoDateLocator()
    >>> formatter = AutoDateFormatter(locator)
    >>> formatter.scaled[1/(24.*60.)] = '%M:%S' # only show min and sec

    A custom `.FuncFormatter` can also be used.  The following example shows
    how to use a custom format function to strip trailing zeros from decimal
    seconds and adds the date to the first ticklabel::

        >>> def my_format_function(x, pos=None):
        ...     x = matplotlib.dates.num2date(x)
        ...     if pos == 0:
        ...         fmt = '%D %H:%M:%S.%f'
        ...     else:
        ...         fmt = '%H:%M:%S.%f'
        ...     label = x.strftime(fmt)
        ...     label = label.rstrip("0")
        ...     label = label.rstrip(".")
        ...     return label
        >>> from matplotlib.ticker import FuncFormatter
        >>> formatter.scaled[1/(24.*60.)] = FuncFormatter(my_format_function)
    """

    # This can be improved by providing some user-level direction on
    # how to choose the best format (precedence, etc...)

    # Perhaps a 'struct' that has a field for each time-type where a
    # zero would indicate "don't show" and a number would indicate
    # "show" with some sort of priority.  Same priorities could mean
    # show all with the same priority.

    # Or more simply, perhaps just a format string for each
    # possibility...

    def __init__(self, locator, tz=None, defaultfmt='%Y-%m-%d', *,
                 usetex=None):
        """
        Autoformat the date labels.

        Parameters
        ----------
        locator : `.ticker.Locator`
            Locator that this axis is using.

        tz : str, optional
            Passed to `.dates.date2num`.

        defaultfmt : str
            The default format to use if none of the values in ``self.scaled``
            are greater than the unit returned by ``locator._get_unit()``.

        usetex : bool, default: :rc:`text.usetex`
            To enable/disable the use of TeX's math mode for rendering the
            results of the formatter. If any entries in ``self.scaled`` are set
            as functions, then it is up to the customized function to enable or
            disable TeX's math mode itself.
        """
        self._locator = locator
        self._tz = tz
        self.defaultfmt = defaultfmt
        self._formatter = DateFormatter(self.defaultfmt, tz)
        rcParams = mpl.rcParams
        self._usetex = (usetex if usetex is not None else
                        mpl.rcParams['text.usetex'])
        self.scaled = {
            DAYS_PER_YEAR: rcParams['date.autoformatter.year'],
            DAYS_PER_MONTH: rcParams['date.autoformatter.month'],
            1: rcParams['date.autoformatter.day'],
            1 / HOURS_PER_DAY: rcParams['date.autoformatter.hour'],
            1 / MINUTES_PER_DAY: rcParams['date.autoformatter.minute'],
            1 / SEC_PER_DAY: rcParams['date.autoformatter.second'],
            1 / MUSECONDS_PER_DAY: rcParams['date.autoformatter.microsecond']
        }

    def _set_locator(self, locator):
        self._locator = locator

    def __call__(self, x, pos=None):
        try:
            locator_unit_scale = float(self._locator._get_unit())
        except AttributeError:
            locator_unit_scale = 1
        # Pick the first scale which is greater than the locator unit.
        fmt = next((fmt for scale, fmt in sorted(self.scaled.items())
                    if scale >= locator_unit_scale),
                   self.defaultfmt)

        if isinstance(fmt, str):
            self._formatter = DateFormatter(fmt, self._tz, usetex=self._usetex)
            result = self._formatter(x, pos)
        elif callable(fmt):
            result = fmt(x, pos)
        else:
            raise TypeError('Unexpected type passed to {0!r}.'.format(self))

        return result
