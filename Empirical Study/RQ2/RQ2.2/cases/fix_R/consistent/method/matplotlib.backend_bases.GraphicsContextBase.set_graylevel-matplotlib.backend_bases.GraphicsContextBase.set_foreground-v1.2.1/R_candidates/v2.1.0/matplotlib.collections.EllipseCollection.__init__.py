    @docstring.dedent_interpd
    def __init__(self, widths, heights, angles, units='points', **kwargs):
        """
        *widths*: sequence
            lengths of first axes (e.g., major axis lengths)

        *heights*: sequence
            lengths of second axes

        *angles*: sequence
            angles of first axes, degrees CCW from the X-axis

        *units*: ['points' | 'inches' | 'dots' | 'width' | 'height'
        | 'x' | 'y' | 'xy']

            units in which majors and minors are given; 'width' and
            'height' refer to the dimensions of the axes, while 'x'
            and 'y' refer to the *offsets* data units. 'xy' differs
            from all others in that the angle as plotted varies with
            the aspect ratio, and equals the specified angle only when
            the aspect ratio is unity.  Hence it behaves the same as
            the :class:`~matplotlib.patches.Ellipse` with
            axes.transData as its transform.

        Additional kwargs inherited from the base :class:`Collection`:

        %(Collection)s
        """
        Collection.__init__(self, **kwargs)
        self._widths = 0.5 * np.asarray(widths).ravel()
        self._heights = 0.5 * np.asarray(heights).ravel()
        self._angles = np.deg2rad(angles).ravel()
        self._units = units
        self.set_transform(transforms.IdentityTransform())
        self._transforms = np.empty((0, 3, 3))
        self._paths = [mpath.Path.unit_circle()]
