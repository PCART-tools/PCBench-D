    def tick_params(self, axis='both', **kwargs):
        """Change the appearance of ticks and tick labels.

        Parameters
        ----------
        axis : {'x', 'y', 'both'}, optional
            Which axis to apply the parameters to.

        Other Parameters
        ----------------

        axis : {'x', 'y', 'both'}
            Axis on which to operate; default is 'both'.

        reset : bool
            If *True*, set all parameters to defaults
            before processing other keyword arguments.  Default is
            *False*.

        which : {'major', 'minor', 'both'}
            Default is 'major'; apply arguments to *which* ticks.

        direction : {'in', 'out', 'inout'}
            Puts ticks inside the axes, outside the axes, or both.

        length : float
            Tick length in points.

        width : float
            Tick width in points.

        color : color
            Tick color; accepts any mpl color spec.

        pad : float
            Distance in points between tick and label.

        labelsize : float or str
            Tick label font size in points or as a string (e.g., 'large').

        labelcolor : color
            Tick label color; mpl color spec.

        colors : color
            Changes the tick color and the label color to the same value:
            mpl color spec.

        zorder : float
            Tick and label zorder.

        bottom, top, left, right : bool or  {'on', 'off'}
            controls whether to draw the respective ticks.

        labelbottom, labeltop, labelleft, labelright : bool or  {'on', 'off'}
            controls whether to draw the
            respective tick labels.

        labelrotation : float
            Tick label rotation

        Examples
        --------

        Usage ::

            ax.tick_params(direction='out', length=6, width=2, colors='r')

        This will make all major ticks be red, pointing out of the box,
        and with dimensions 6 points by 2 points.  Tick labels will
        also be red.

        """
        if axis in ['x', 'both']:
            xkw = dict(kwargs)
            xkw.pop('left', None)
            xkw.pop('right', None)
            xkw.pop('labelleft', None)
            xkw.pop('labelright', None)
            self.xaxis.set_tick_params(**xkw)
        if axis in ['y', 'both']:
            ykw = dict(kwargs)
            ykw.pop('top', None)
            ykw.pop('bottom', None)
            ykw.pop('labeltop', None)
            ykw.pop('labelbottom', None)
            self.yaxis.set_tick_params(**ykw)
