    @_preprocess_data(replace_names=["x", "y"], label_namer="y")
    def step(self, x, y, *args, **kwargs):
        """
        Make a step plot.

        Parameters
        ----------
        x : array_like
            1-D sequence, and it is assumed, but not checked,
            that it is uniformly increasing.

        y : array_like
            1-D sequence

        Returns
        -------
        list
            List of lines that were added.

        Other Parameters
        ----------------
        where : [ 'pre' | 'post' | 'mid'  ]
            If 'pre' (the default), the interval from
            ``x[i]`` to ``x[i+1]`` has level ``y[i+1]``.

            If 'post', that interval has level ``y[i]``.

            If 'mid', the jumps in *y* occur half-way between the
            *x*-values.

        Notes
        -----
        Additional parameters are the same as those for
        :func:`~matplotlib.pyplot.plot`.
        """

        where = kwargs.pop('where', 'pre')
        if where not in ('pre', 'post', 'mid'):
            raise ValueError("'where' argument to step must be "
                             "'pre', 'post' or 'mid'")
        usr_linestyle = kwargs.pop('linestyle', '')
        kwargs['linestyle'] = 'steps-' + where + usr_linestyle

        return self.plot(x, y, *args, **kwargs)
