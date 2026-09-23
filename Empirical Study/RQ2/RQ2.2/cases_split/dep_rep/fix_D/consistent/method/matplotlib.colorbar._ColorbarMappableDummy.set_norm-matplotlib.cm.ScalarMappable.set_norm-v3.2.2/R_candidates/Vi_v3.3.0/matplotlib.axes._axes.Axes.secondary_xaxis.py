    @docstring.dedent_interpd
    def secondary_xaxis(self, location, *, functions=None, **kwargs):
        """
        Add a second x-axis to this axes.

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
                return 1 / x

            secax = ax.secondary_xaxis('top', functions=(invert, invert))
            secax.set_xlabel('Period [s]')
            plt.show()
        """
        if location in ['top', 'bottom'] or isinstance(location, Number):
            secondary_ax = SecondaryAxis(self, 'x', location, functions,
                                         **kwargs)
            self.add_child_axes(secondary_ax)
            return secondary_ax
        else:
            raise ValueError('secondary_xaxis location must be either '
                             'a float or "top"/"bottom"')
