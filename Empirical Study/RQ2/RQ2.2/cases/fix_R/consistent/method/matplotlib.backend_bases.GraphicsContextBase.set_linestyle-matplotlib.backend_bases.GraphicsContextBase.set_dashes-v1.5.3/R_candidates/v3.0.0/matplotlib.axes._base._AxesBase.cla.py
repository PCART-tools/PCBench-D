    def cla(self):
        """Clear the current axes."""
        # Note: this is called by Axes.__init__()

        # stash the current visibility state
        if hasattr(self, 'patch'):
            patch_visible = self.patch.get_visible()
        else:
            patch_visible = True

        xaxis_visible = self.xaxis.get_visible()
        yaxis_visible = self.yaxis.get_visible()

        self.xaxis.cla()
        self.yaxis.cla()

        for name, spine in self.spines.items():
            spine.cla()

        self.ignore_existing_data_limits = True
        self.callbacks = cbook.CallbackRegistry()

        if self._sharex is not None:
            # major and minor are axis.Ticker class instances with
            # locator and formatter attributes
            self.xaxis.major = self._sharex.xaxis.major
            self.xaxis.minor = self._sharex.xaxis.minor
            x0, x1 = self._sharex.get_xlim()
            self.set_xlim(x0, x1, emit=False,
                          auto=self._sharex.get_autoscalex_on())
            self.xaxis._scale = mscale.scale_factory(
                    self._sharex.xaxis.get_scale(), self.xaxis)
        else:
            self.xaxis._set_scale('linear')
            try:
                self.set_xlim(0, 1)
            except TypeError:
                pass

        if self._sharey is not None:
            self.yaxis.major = self._sharey.yaxis.major
            self.yaxis.minor = self._sharey.yaxis.minor
            y0, y1 = self._sharey.get_ylim()
            self.set_ylim(y0, y1, emit=False,
                          auto=self._sharey.get_autoscaley_on())
            self.yaxis._scale = mscale.scale_factory(
                    self._sharey.yaxis.get_scale(), self.yaxis)
        else:
            self.yaxis._set_scale('linear')
            try:
                self.set_ylim(0, 1)
            except TypeError:
                pass
        # update the minor locator for x and y axis based on rcParams
        if rcParams['xtick.minor.visible']:
            self.xaxis.set_minor_locator(mticker.AutoMinorLocator())

        if rcParams['ytick.minor.visible']:
            self.yaxis.set_minor_locator(mticker.AutoMinorLocator())

        if self._sharex is None:
            self._autoscaleXon = True
        if self._sharey is None:
            self._autoscaleYon = True
        self._xmargin = rcParams['axes.xmargin']
        self._ymargin = rcParams['axes.ymargin']
        self._tight = None
        self._use_sticky_edges = True
        self._update_transScale()  # needed?

        self._get_lines = _process_plot_var_args(self)
        self._get_patches_for_fill = _process_plot_var_args(self, 'fill')

        self._gridOn = rcParams['axes.grid']
        self.lines = []
        self.patches = []
        self.texts = []
        self.tables = []
        self.artists = []
        self.images = []
        self._mouseover_set = _OrderedSet()
        self.child_axes = []
        self._current_image = None  # strictly for pyplot via _sci, _gci
        self.legend_ = None
        self.collections = []  # collection.Collection instances
        self.containers = []

        self.grid(False)  # Disable grid on init to use rcParameter
        self.grid(self._gridOn, which=rcParams['axes.grid.which'],
                  axis=rcParams['axes.grid.axis'])
        props = font_manager.FontProperties(
            size=rcParams['axes.titlesize'],
            weight=rcParams['axes.titleweight'])

        self.title = mtext.Text(
            x=0.5, y=1.0, text='',
            fontproperties=props,
            verticalalignment='baseline',
            horizontalalignment='center',
            )
        self._left_title = mtext.Text(
            x=0.0, y=1.0, text='',
            fontproperties=props.copy(),
            verticalalignment='baseline',
            horizontalalignment='left', )
        self._right_title = mtext.Text(
            x=1.0, y=1.0, text='',
            fontproperties=props.copy(),
            verticalalignment='baseline',
            horizontalalignment='right',
            )
        title_offset_points = rcParams['axes.titlepad']
        # refactor this out so it can be called in ax.set_title if
        # pad argument used...
        self._set_title_offset_trans(title_offset_points)
        # determine if the title position has been set manually:
        self._autotitlepos = None

        for _title in (self.title, self._left_title, self._right_title):
            self._set_artist_props(_title)

        # The patch draws the background of the axes.  We want this to be below
        # the other artists.  We use the frame to draw the edges so we are
        # setting the edgecolor to None.
        self.patch = self._gen_axes_patch()
        self.patch.set_figure(self.figure)
        self.patch.set_facecolor(self._facecolor)
        self.patch.set_edgecolor('None')
        self.patch.set_linewidth(0)
        self.patch.set_transform(self.transAxes)

        self.set_axis_on()

        self.xaxis.set_clip_path(self.patch)
        self.yaxis.set_clip_path(self.patch)

        self._shared_x_axes.clean()
        self._shared_y_axes.clean()
        if self._sharex:
            self.xaxis.set_visible(xaxis_visible)
            self.patch.set_visible(patch_visible)

        if self._sharey:
            self.yaxis.set_visible(yaxis_visible)
            self.patch.set_visible(patch_visible)

        self.stale = True
