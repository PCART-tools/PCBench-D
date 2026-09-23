    def __init__(self, *args, **kwargs):
        """
        Keyword args:

        *nbins*
            Maximum number of intervals; one less than max number of
            ticks.  If the string `'auto'`, the number of bins will be
            automatically determined based on the length of the axis.

        *steps*
            Sequence of nice numbers starting with 1 and ending with 10;
            e.g., [1, 2, 4, 5, 10]

        *integer*
            If True, ticks will take only integer values, provided
            at least `min_n_ticks` integers are found within the
            view limits.

        *symmetric*
            If True, autoscaling will result in a range symmetric
            about zero.

        *prune*
            ['lower' | 'upper' | 'both' | None]
            Remove edge ticks -- useful for stacked or ganged plots
            where the upper tick of one axes overlaps with the lower
            tick of the axes above it, primarily when
            `rcParams['axes.autolimit_mode']` is `'round_numbers'`.
            If `prune=='lower'`, the smallest tick will
            be removed.  If `prune=='upper'`, the largest tick will be
            removed.  If `prune=='both'`, the largest and smallest ticks
            will be removed.  If `prune==None`, no ticks will be removed.

        *min_n_ticks*
            Relax `nbins` and `integer` constraints if necessary to
            obtain this minimum number of ticks.

        """
        if args:
            kwargs['nbins'] = args[0]
            if len(args) > 1:
                raise ValueError(
                    "Keywords are required for all arguments except 'nbins'")
        self.set_params(**self.default_params)
        self.set_params(**kwargs)
