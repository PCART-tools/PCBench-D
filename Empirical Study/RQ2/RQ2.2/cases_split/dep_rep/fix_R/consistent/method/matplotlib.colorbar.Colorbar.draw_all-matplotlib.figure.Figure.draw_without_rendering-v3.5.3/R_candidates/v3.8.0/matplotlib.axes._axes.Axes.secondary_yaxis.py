    @_docstring.dedent_interpd
    def secondary_yaxis(self, location, *, functions=None, **kwargs):
        """
        Add a second y-axis to this `~.axes.Axes`.

        For example if we want to have a second scale for the data plotted on
        the yaxis.

        %(_secax_docstring)s

        Examples
        --------
        Add a secondary Axes that converts from radians to degrees

        .. plot::

            fig, ax = plt.subplots()
            ax.plot(range(1, 360, 5), range(1, 360, 5))
            ax.set_ylabel('degrees')
            secax = ax.secondary_yaxis('right', functions=(np.deg2rad,
                                                           np.rad2deg))
            secax.set_ylabel('radians')
        """
        if location in ['left', 'right'] or isinstance(location, Real):
            secondary_ax = SecondaryAxis(self, 'y', location,
                                         functions, **kwargs)
            self.add_child_axes(secondary_ax)
            return secondary_ax
        else:
            raise ValueError('secondary_yaxis location must be either '
                             'a float or "left"/"right"')
