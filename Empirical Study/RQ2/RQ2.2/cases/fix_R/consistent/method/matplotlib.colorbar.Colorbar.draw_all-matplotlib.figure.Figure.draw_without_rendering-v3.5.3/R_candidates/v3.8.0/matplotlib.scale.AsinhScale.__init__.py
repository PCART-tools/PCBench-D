    def __init__(self, axis, *, linear_width=1.0,
                 base=10, subs='auto', **kwargs):
        """
        Parameters
        ----------
        linear_width : float, default: 1
            The scale parameter (elsewhere referred to as :math:`a_0`)
            defining the extent of the quasi-linear region,
            and the coordinate values beyond which the transformation
            becomes asymptotically logarithmic.
        base : int, default: 10
            The number base used for rounding tick locations
            on a logarithmic scale. If this is less than one,
            then rounding is to the nearest integer multiple
            of powers of ten.
        subs : sequence of int
            Multiples of the number base used for minor ticks.
            If set to 'auto', this will use built-in defaults,
            e.g. (2, 5) for base=10.
        """
        super().__init__(axis)
        self._transform = AsinhTransform(linear_width)
        self._base = int(base)
        if subs == 'auto':
            self._subs = self.auto_tick_multipliers.get(self._base)
        else:
            self._subs = subs
