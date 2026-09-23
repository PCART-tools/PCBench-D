    def add_subplot(self, *args, **kwargs):
        """
        Add a subplot.

        Parameters
        ----------
        *args
            Either a 3-digit integer or three separate integers
            describing the position of the subplot. If the three
            integers are I, J, and K, the subplot is the Ith plot on a
            grid with J rows and K columns.

        projection : ['aitoff' | 'hammer' | 'lambert' | \
'mollweide', 'polar' | 'rectilinear'], optional
            The projection type of the axes.

        polar : boolean, optional
            If True, equivalent to projection='polar'.

        This method also takes the keyword arguments for
        :class:`~matplotlib.axes.Axes`.

        Returns
        -------
        axes : Axes
            The axes of the subplot.

        Notes
        -----
        If the figure already has a subplot with key (*args*,
        *kwargs*) then it will simply make that subplot current and
        return it.  This behavior is deprecated.

        Examples
        --------
            fig.add_subplot(111)

            # equivalent but more general
            fig.add_subplot(1, 1, 1)

            # add subplot with red background
            fig.add_subplot(212, facecolor='r')

            # add a polar subplot
            fig.add_subplot(111, projection='polar')

            # add Subplot instance sub
            fig.add_subplot(sub)

        See Also
        --------
        matplotlib.pyplot.subplot : for an explanation of the args.
        """
        if not len(args):
            return

        if len(args) == 1 and isinstance(args[0], int):
            if not 100 <= args[0] <= 999:
                raise ValueError("Integer subplot specification must be a "
                                 "three-digit number, not {}".format(args[0]))
            args = tuple(map(int, str(args[0])))

        if isinstance(args[0], SubplotBase):

            a = args[0]
            if a.get_figure() is not self:
                msg = ("The Subplot must have been created in the present "
                       "figure")
                raise ValueError(msg)
            # make a key for the subplot (which includes the axes object id
            # in the hash)
            key = self._make_key(*args, **kwargs)
        else:
            projection_class, kwargs, key = process_projection_requirements(
                self, *args, **kwargs)

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

        self._axstack.add(key, a)
        self.sca(a)
        a._remove_method = self.__remove_ax
        self.stale = True
        a.stale_callback = _stale_figure_callback
        return a
