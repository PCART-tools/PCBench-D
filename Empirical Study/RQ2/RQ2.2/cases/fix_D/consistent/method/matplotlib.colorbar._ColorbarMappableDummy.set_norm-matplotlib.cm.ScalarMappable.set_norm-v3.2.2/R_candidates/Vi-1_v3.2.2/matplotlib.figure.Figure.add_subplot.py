    @docstring.dedent_interpd
    def add_subplot(self, *args, **kwargs):
        """
        Add an `~.axes.Axes` to the figure as part of a subplot arrangement.

        Call signatures::

           add_subplot(nrows, ncols, index, **kwargs)
           add_subplot(pos, **kwargs)
           add_subplot(ax)
           add_subplot()

        Parameters
        ----------
        *args
            Either a 3-digit integer or three separate integers
            describing the position of the subplot. If the three
            integers are *nrows*, *ncols*, and *index* in order, the
            subplot will take the *index* position on a grid with *nrows*
            rows and *ncols* columns. *index* starts at 1 in the upper left
            corner and increases to the right.

            *pos* is a three digit integer, where the first digit is the
            number of rows, the second the number of columns, and the third
            the index of the subplot. i.e. fig.add_subplot(235) is the same as
            fig.add_subplot(2, 3, 5). Note that all integers must be less than
            10 for this form to work.

            If no positional arguments are passed, defaults to (1, 1, 1).

            In rare circumstances, `.add_subplot` may be called with a single
            argument, a subplot axes instance already created in the
            present figure but not in the figure's list of axes.

        projection : {None, 'aitoff', 'hammer', 'lambert', 'mollweide', \
'polar', 'rectilinear', str}, optional
            The projection type of the subplot (`~.axes.Axes`). *str* is the
            name of a custom projection, see `~matplotlib.projections`. The
            default None results in a 'rectilinear' projection.

        polar : boolean, optional
            If True, equivalent to projection='polar'.

        sharex, sharey : `~.axes.Axes`, optional
            Share the x or y `~matplotlib.axis` with sharex and/or sharey.
            The axis will have the same limits, ticks, and scale as the axis
            of the shared axes.

        label : str
            A label for the returned axes.

        Other Parameters
        ----------------
        **kwargs
            This method also takes the keyword arguments for the returned axes
            base class; except for the *figure* argument. The keyword arguments
            for the rectilinear base class `~.axes.Axes` can be found in
            the following table but there might also be other keyword
            arguments if another projection is used.

            %(Axes)s

        Returns
        -------
        axes : `.axes.SubplotBase`, or another subclass of `~.axes.Axes`

            The axes of the subplot. The returned axes base class depends on
            the projection used. It is `~.axes.Axes` if rectilinear projection
            are used and `.projections.polar.PolarAxes` if polar projection
            are used. The returned axes is then a subplot subclass of the
            base class.

        Notes
        -----
        If the figure already has a subplot with key (*args*,
        *kwargs*) then it will simply make that subplot current and
        return it.  This behavior is deprecated. Meanwhile, if you do
        not want this behavior (i.e., you want to force the creation of a
        new subplot), you must use a unique set of args and kwargs.  The axes
        *label* attribute has been exposed for this purpose: if you want
        two subplots that are otherwise identical to be added to the figure,
        make sure you give them unique labels.

        See Also
        --------
        .Figure.add_axes
        .pyplot.subplot
        .pyplot.axes
        .Figure.subplots
        .pyplot.subplots

        Examples
        --------
        ::

            fig = plt.figure()
            fig.add_subplot(221)

            # equivalent but more general
            ax1 = fig.add_subplot(2, 2, 1)

            # add a subplot with no frame
            ax2 = fig.add_subplot(222, frameon=False)

            # add a polar subplot
            fig.add_subplot(223, projection='polar')

            # add a red subplot that share the x-axis with ax1
            fig.add_subplot(224, sharex=ax1, facecolor='red')

            #delete x2 from the figure
            fig.delaxes(ax2)

            #add x2 to the figure again
            fig.add_subplot(ax2)
        """
        if not len(args):
            args = (1, 1, 1)

        if len(args) == 1 and isinstance(args[0], Integral):
            if not 100 <= args[0] <= 999:
                raise ValueError("Integer subplot specification must be a "
                                 "three-digit number, not {}".format(args[0]))
            args = tuple(map(int, str(args[0])))

        if 'figure' in kwargs:
            # Axes itself allows for a 'figure' kwarg, but since we want to
            # bind the created Axes to self, it is not allowed here.
            raise TypeError(
                "add_subplot() got an unexpected keyword argument 'figure'")

        if isinstance(args[0], SubplotBase):

            a = args[0]
            if a.get_figure() is not self:
                raise ValueError(
                    "The Subplot must have been created in the present figure")
            # make a key for the subplot (which includes the axes object id
            # in the hash)
            key = self._make_key(*args, **kwargs)
        else:
            projection_class, kwargs, key = \
                self._process_projection_requirements(*args, **kwargs)

            # try to find the axes with this key in the stack
            ax = self._axstack.get(key)

            if ax is not None:
                if isinstance(ax, projection_class):
                    # the axes already existed, so set it as active & return
                    self.sca(ax)
                    return ax
                else:
                    # Undocumented convenience behavior:
                    # subplot(111); subplot(111, projection='polar')
                    # will replace the first with the second.
                    # Without this, add_subplot would be simpler and
                    # more similar to add_axes.
                    self._axstack.remove(ax)

            a = subplot_class_factory(projection_class)(self, *args, **kwargs)

        return self._add_axes_internal(key, a)
