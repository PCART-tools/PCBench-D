    @docstring.dedent_interpd
    def add_axes(self, *args, **kwargs):
        """
        Add an axes to the figure.

        Call signatures::

            add_axes(rect, projection=None, polar=False, **kwargs)
            add_axes(ax)

        Parameters
        ----------

        rect : sequence of float
            The dimensions [left, bottom, width, height] of the new axes. All
            quantities are in fractions of figure width and height.

        projection : {None, 'aitoff', 'hammer', 'lambert', 'mollweide', \
'polar', 'rectilinear', str}, optional
            The projection type of the `~.axes.Axes`. *str* is the name of
            a custom projection, see `~matplotlib.projections`. The default
            None results in a 'rectilinear' projection.

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
            This method also takes the keyword arguments for
            the returned axes class. The keyword arguments for the
            rectilinear axes class `~.axes.Axes` can be found in
            the following table but there might also be other keyword
            arguments if another projection is used, see the actual axes
            class.
            %(Axes)s

        Returns
        -------
        axes : `~.axes.Axes` (or a subclass of `~.axes.Axes`)
            The returned axes class depends on the projection used. It is
            `~.axes.Axes` if rectilinear projection are used and
            `.projections.polar.PolarAxes` if polar projection
            are used.

        Notes
        -----
        If the figure already has an axes with key (*args*,
        *kwargs*) then it will simply make that axes current and
        return it.  This behavior is deprecated. Meanwhile, if you do
        not want this behavior (i.e., you want to force the creation of a
        new axes), you must use a unique set of args and kwargs.  The axes
        *label* attribute has been exposed for this purpose: if you want
        two axes that are otherwise identical to be added to the figure,
        make sure you give them unique labels.

        In rare circumstances, `.add_axes` may be called with a single
        argument, a axes instance already created in the present figure but
        not in the figure's list of axes.

        See Also
        --------
        .Figure.add_subplot
        .pyplot.subplot
        .pyplot.axes
        .Figure.subplots
        .pyplot.subplots

        Examples
        --------
        Some simple examples::

            rect = l, b, w, h
            fig = plt.figure()
            fig.add_axes(rect,label=label1)
            fig.add_axes(rect,label=label2)
            fig.add_axes(rect, frameon=False, facecolor='g')
            fig.add_axes(rect, polar=True)
            ax=fig.add_axes(rect, projection='polar')
            fig.delaxes(ax)
            fig.add_axes(ax)
        """

        if not len(args):
            return

        # shortcut the projection "key" modifications later on, if an axes
        # with the exact args/kwargs exists, return it immediately.
        key = self._make_key(*args, **kwargs)
        ax = self._axstack.get(key)
        if ax is not None:
            self.sca(ax)
            return ax

        if isinstance(args[0], Axes):
            a = args[0]
            if a.get_figure() is not self:
                raise ValueError(
                    "The Axes must have been created in the present figure")
        else:
            rect = args[0]
            if not np.isfinite(rect).all():
                raise ValueError('all entries in rect must be finite '
                                 'not {}'.format(rect))
            projection_class, kwargs, key = \
                self._process_projection_requirements(*args, **kwargs)

            # check that an axes of this type doesn't already exist, if it
            # does, set it as active and return it
            ax = self._axstack.get(key)
            if isinstance(ax, projection_class):
                self.sca(ax)
                return ax

            # create the new axes using the axes class given
            a = projection_class(self, rect, **kwargs)

        return self._add_axes_internal(key, a)
