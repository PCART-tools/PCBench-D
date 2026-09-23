    def add_axes(self, *args, **kwargs):
        """
        Add an axes at position *rect* [*left*, *bottom*, *width*,
        *height*] where all quantities are in fractions of figure
        width and height.

        Parameters
        ----------
        rect : sequence of float
            A 4-length sequence of [left, bottom, width, height] quantities.

        projection :
            ['aitoff' | 'hammer' | 'lambert' | 'mollweide' | \
'polar' | 'rectilinear'], optional
            The projection type of the axes.

        polar : boolean, optional
            If True, equivalent to projection='polar'.

        This method also takes the keyword arguments for
        :class:`~matplotlib.axes.Axes`.

        Returns
        ------
        axes : Axes
            The added axes.

        Examples
        --------
        A simple example::

            rect = l,b,w,h
            fig.add_axes(rect)
            fig.add_axes(rect, frameon=False, facecolor='g')
            fig.add_axes(rect, polar=True)
            fig.add_axes(rect, projection='polar')
            fig.add_axes(ax)

        If the figure already has an axes with the same parameters, then it
        will simply make that axes current and return it.  This behavior
        has been deprecated as of Matplotlib 2.1.  Meanwhile, if you do
        not want this behavior (i.e., you want to force the creation of a
        new Axes), you must use a unique set of args and kwargs.  The axes
        :attr:`~matplotlib.axes.Axes.label` attribute has been exposed for this
        purpose: if you want two axes that are otherwise identical to be added
        to the figure, make sure you give them unique labels::

            fig.add_axes(rect, label='axes1')
            fig.add_axes(rect, label='axes2')

        In rare circumstances, add_axes may be called with a single
        argument, an Axes instance already created in the present
        figure but not in the figure's list of axes.  For example,
        if an axes has been removed with :meth:`delaxes`, it can
        be restored with::

            fig.add_axes(ax)

        In all cases, the :class:`~matplotlib.axes.Axes` instance
        will be returned.
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
                msg = "The Axes must have been created in the present figure"
                raise ValueError(msg)
        else:
            rect = args[0]
            if not np.isfinite(rect).all():
                raise ValueError('all entries in rect must be finite '
                                 'not {}'.format(rect))
            projection_class, kwargs, key = process_projection_requirements(
                self, *args, **kwargs)

            # check that an axes of this type doesn't already exist, if it
            # does, set it as active and return it
            ax = self._axstack.get(key)
            if isinstance(ax, projection_class):
                self.sca(ax)
                return ax

            # create the new axes using the axes class given
            a = projection_class(self, rect, **kwargs)

        self._axstack.add(key, a)
        self.sca(a)
        a._remove_method = self.__remove_ax
        self.stale = True
        a.stale_callback = _stale_figure_callback
        return a
