    @_docstring.interpd
    def secondary_xaxis(self, location, functions=None, *, transform=None, **kwargs):
        """
        Add a second x-axis to this `~.axes.Axes`.

        For example if we want to have a second scale for the data plotted on
        the xaxis.

        %(_secax_docstring)s

        Examples
        --------
        The main axis shows frequency, and the secondary axis shows period.

        .. plot::

            fig, ax = plt.subplots()
            ax.loglog(range(1, 360, 5), range(1, 360, 5))
            ax.set_xlabel('frequency [Hz]')

            def invert(x):
                # 1/x with special treatment of x == 0
                x = np.array(x).astype(float)
                near_zero = np.isclose(x, 0)
                x[near_zero] = np.inf
                x[~near_zero] = 1 / x[~near_zero]
                return x

            # the inverse of 1/x is itself
            secax = ax.secondary_xaxis('top', functions=(invert, invert))
            secax.set_xlabel('Period [s]')
            plt.show()

        To add a secondary axis relative to your data, you can pass a transform
        to the new axis.

        .. plot::

            fig, ax = plt.subplots()
            ax.plot(range(0, 5), range(-1, 4))

            # Pass 'ax.transData' as a transform to place the axis
            # relative to your data at y=0
            secax = ax.secondary_xaxis(0, transform=ax.transData)
        """
        if not (location in ['top', 'bottom'] or isinstance(location, Real)):
            raise ValueError('secondary_xaxis location must be either '
                             'a float or "top"/"bottom"')

        secondary_ax = SecondaryAxis(self, 'x', location, functions,
                                     transform, **kwargs)
        self.add_child_axes(secondary_ax)
        return secondary_ax
