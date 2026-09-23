class SymmetricalLogLocator(Locator):
    """
    Determine the tick locations for symmetric log axes.
    """

    def __init__(self, transform=None, subs=None, linthresh=None, base=None):
        """
        Parameters
        ----------
        transform : `~.scale.SymmetricalLogTransform`, optional
            If set, defines the *base* and *linthresh* of the symlog transform.
        base, linthresh : float, optional
            The *base* and *linthresh* of the symlog transform, as documented
            for `.SymmetricalLogScale`.  These parameters are only used if
            *transform* is not set.
        subs : sequence of float, default: [1]
            The multiples of integer powers of the base where ticks are placed,
            i.e., ticks are placed at
            ``[sub * base**i for i in ... for sub in subs]``.

        Notes
        -----
        Either *transform*, or both *base* and *linthresh*, must be given.
        """
        if transform is not None:
            self._base = transform.base
            self._linthresh = transform.linthresh
        elif linthresh is not None and base is not None:
            self._base = base
            self._linthresh = linthresh
        else:
            raise ValueError("Either transform, or both linthresh "
                             "and base, must be provided.")
        if subs is None:
            self._subs = [1.0]
        else:
            self._subs = subs
        self.numticks = 15

    def set_params(self, subs=None, numticks=None):
        """Set parameters within this locator."""
        if numticks is not None:
            self.numticks = numticks
        if subs is not None:
            self._subs = subs

    def __call__(self):
        """Return the locations of the ticks."""
        # Note, these are untransformed coordinates
        vmin, vmax = self.axis.get_view_interval()
        return self.tick_values(vmin, vmax)

    def tick_values(self, vmin, vmax):
        base = self._base
        linthresh = self._linthresh

        if vmax < vmin:
            vmin, vmax = vmax, vmin

        # The domain is divided into three sections, only some of
        # which may actually be present.
        #
        # <======== -t ==0== t ========>
        # aaaaaaaaa    bbbbb   ccccccccc
        #
        # a) and c) will have ticks at integral log positions.  The
        # number of ticks needs to be reduced if there are more
        # than self.numticks of them.
        #
        # b) has a tick at 0 and only 0 (we assume t is a small
        # number, and the linear segment is just an implementation
        # detail and not interesting.)
        #
        # We could also add ticks at t, but that seems to usually be
        # uninteresting.
        #
        # "simple" mode is when the range falls entirely within (-t,
        # t) -- it should just display (vmin, 0, vmax)
        if -linthresh < vmin < vmax < linthresh:
            # only the linear range is present
            return [vmin, vmax]

        # Lower log range is present
        has_a = (vmin < -linthresh)
        # Upper log range is present
        has_c = (vmax > linthresh)

        # Check if linear range is present
        has_b = (has_a and vmax > -linthresh) or (has_c and vmin < linthresh)

        def get_log_range(lo, hi):
            lo = np.floor(np.log(lo) / np.log(base))
            hi = np.ceil(np.log(hi) / np.log(base))
            return lo, hi

        # Calculate all the ranges, so we can determine striding
        a_lo, a_hi = (0, 0)
        if has_a:
            a_upper_lim = min(-linthresh, vmax)
            a_lo, a_hi = get_log_range(abs(a_upper_lim), abs(vmin) + 1)

        c_lo, c_hi = (0, 0)
        if has_c:
            c_lower_lim = max(linthresh, vmin)
            c_lo, c_hi = get_log_range(c_lower_lim, vmax + 1)

        # Calculate the total number of integer exponents in a and c ranges
        total_ticks = (a_hi - a_lo) + (c_hi - c_lo)
        if has_b:
            total_ticks += 1
        stride = max(total_ticks // (self.numticks - 1), 1)

        decades = []
        if has_a:
            decades.extend(-1 * (base ** (np.arange(a_lo, a_hi,
                                                    stride)[::-1])))

        if has_b:
            decades.append(0.0)

        if has_c:
            decades.extend(base ** (np.arange(c_lo, c_hi, stride)))

        # Add the subticks if requested
        if self._subs is None:
            subs = np.arange(2.0, base)
        else:
            subs = np.asarray(self._subs)

        if len(subs) > 1 or subs[0] != 1.0:
            ticklocs = []
            for decade in decades:
                if decade == 0:
                    ticklocs.append(decade)
                else:
                    ticklocs.extend(subs * decade)
        else:
            ticklocs = decades

        return self.raise_if_exceeds(np.array(ticklocs))

    def view_limits(self, vmin, vmax):
        """Try to choose the view limits intelligently."""
        b = self._base
        if vmax < vmin:
            vmin, vmax = vmax, vmin

        if mpl.rcParams['axes.autolimit_mode'] == 'round_numbers':
            vmin = _decade_less_equal(vmin, b)
            vmax = _decade_greater_equal(vmax, b)
            if vmin == vmax:
                vmin = _decade_less(vmin, b)
                vmax = _decade_greater(vmax, b)

        result = mtransforms.nonsingular(vmin, vmax)
        return result
