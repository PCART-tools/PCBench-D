    @docstring.dedent_interpd
    def __init__(self, axes, spine_type, path, **kwargs):
        """
        Parameters
        ----------
        axes : `~matplotlib.axes.Axes`
            The `~.axes.Axes` instance containing the spine.
        spine_type : str
            The spine type.
        path : `~matplotlib.path.Path`
            The `.Path` instance used to draw the spine.

        Other Parameters
        ----------------
        **kwargs
            Valid keyword arguments are:

            %(Patch:kwdoc)s
        """
        super().__init__(**kwargs)
        self.axes = axes
        self.set_figure(self.axes.figure)
        self.spine_type = spine_type
        self.set_facecolor('none')
        self.set_edgecolor(rcParams['axes.edgecolor'])
        self.set_linewidth(rcParams['axes.linewidth'])
        self.set_capstyle('projecting')
        self.axis = None

        self.set_zorder(2.5)
        self.set_transform(self.axes.transData)  # default transform

        self._bounds = None  # default bounds

        # Defer initial position determination. (Not much support for
        # non-rectangular axes is currently implemented, and this lets
        # them pass through the spines machinery without errors.)
        self._position = None
        _api.check_isinstance(matplotlib.path.Path, path=path)
        self._path = path

        # To support drawing both linear and circular spines, this
        # class implements Patch behavior three ways. If
        # self._patch_type == 'line', behave like a mpatches.PathPatch
        # instance. If self._patch_type == 'circle', behave like a
        # mpatches.Ellipse instance. If self._patch_type == 'arc', behave like
        # a mpatches.Arc instance.
        self._patch_type = 'line'

        # Behavior copied from mpatches.Ellipse:
        # Note: This cannot be calculated until this is added to an Axes
        self._patch_transform = mtransforms.IdentityTransform()
