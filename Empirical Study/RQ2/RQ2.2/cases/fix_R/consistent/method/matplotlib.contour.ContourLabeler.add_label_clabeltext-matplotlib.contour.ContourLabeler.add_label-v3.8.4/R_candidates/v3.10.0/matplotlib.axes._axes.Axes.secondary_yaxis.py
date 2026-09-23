    @_docstring.interpd
    def secondary_yaxis(self, location, functions=None, *, transform=None, **kwargs):
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

        To add a secondary axis relative to your data, you can pass a transform
        to the new axis.

        .. plot::

            fig, ax = plt.subplots()
            ax.plot(range(0, 5), range(-1, 4))

            # Pass 'ax.transData' as a transform to place the axis
            # relative to your data at x=3
            secax = ax.secondary_yaxis(3, transform=ax.transData)
        """
        if not (location in ['left', 'right'] or isinstance(location, Real)):
            raise ValueError('secondary_yaxis location must be either '
                             'a float or "left"/"right"')

        secondary_ax = SecondaryAxis(self, 'y', location, functions,
                                     transform, **kwargs)
        self.add_child_axes(secondary_ax)
        return secondary_ax
