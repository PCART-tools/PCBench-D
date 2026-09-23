class Axis(martist.Artist):
    """
    Base class for `.XAxis` and `.YAxis`.

    Attributes
    ----------
    isDefault_label : bool

    axes : `matplotlib.axes.Axes`
        The `~.axes.Axes` to which the Axis belongs.
    major : `matplotlib.axis.Ticker`
        Determines the major tick positions and their label format.
    minor : `matplotlib.axis.Ticker`
        Determines the minor tick positions and their label format.
    callbacks : `matplotlib.cbook.CallbackRegistry`

    label : `.Text`
        The axis label.
    labelpad : float
        The distance between the axis label and the tick labels.
        Defaults to :rc:`axes.labelpad` = 4.
    offsetText : `.Text`
        A `.Text` object containing the data offset of the ticks (if any).
    pickradius : float
        The acceptance radius for containment tests. See also `.Axis.contains`.
    majorTicks : list of `.Tick`
        The major ticks.
    minorTicks : list of `.Tick`
        The minor ticks.
    """
    OFFSETTEXTPAD = 3

    def __str__(self):
        return "{}({},{})".format(
            type(self).__name__, *self.axes.transAxes.transform((0, 0)))

    def __init__(self, axes, pickradius=15):
        """
        Parameters
        ----------
        axes : `matplotlib.axes.Axes`
            The `~.axes.Axes` to which the created Axis belongs.
        pickradius : float
            The acceptance radius for containment tests. See also
            `.Axis.contains`.
        """
        super().__init__()
        self._remove_overlapping_locs = True

        self.set_figure(axes.figure)

        self.isDefault_label = True

        self.axes = axes
        self.major = Ticker()
        self.minor = Ticker()
        self.callbacks = cbook.CallbackRegistry()

        self._autolabelpos = True

        self.label = mtext.Text(
            np.nan, np.nan,
            fontsize=mpl.rcParams['axes.labelsize'],
            fontweight=mpl.rcParams['axes.labelweight'],
            color=mpl.rcParams['axes.labelcolor'],
        )
        self._set_artist_props(self.label)
        self.offsetText = mtext.Text(np.nan, np.nan)
        self._set_artist_props(self.offsetText)

        self.labelpad = mpl.rcParams['axes.labelpad']

        self.pickradius = pickradius

        # Initialize here for testing; later add API
        self._major_tick_kw = dict()
        self._minor_tick_kw = dict()

        self.clear()
        self._set_scale('linear')

    @property
    def isDefault_majloc(self):
        return self.major._locator_is_default

    @isDefault_majloc.setter
    def isDefault_majloc(self, value):
        self.major._locator_is_default = value

    @property
    def isDefault_majfmt(self):
        return self.major._formatter_is_default

    @isDefault_majfmt.setter
    def isDefault_majfmt(self, value):
        self.major._formatter_is_default = value

    @property
    def isDefault_minloc(self):
        return self.minor._locator_is_default

    @isDefault_minloc.setter
    def isDefault_minloc(self, value):
        self.minor._locator_is_default = value

    @property
    def isDefault_minfmt(self):
        return self.minor._formatter_is_default

    @isDefault_minfmt.setter
    def isDefault_minfmt(self, value):
        self.minor._formatter_is_default = value

    # During initialization, Axis objects often create ticks that are later
    # unused; this turns out to be a very slow step.  Instead, use a custom
    # descriptor to make the tick lists lazy and instantiate them as needed.
    majorTicks = _LazyTickList(major=True)
    minorTicks = _LazyTickList(major=False)

    def get_remove_overlapping_locs(self):
        return self._remove_overlapping_locs

    def set_remove_overlapping_locs(self, val):
        self._remove_overlapping_locs = bool(val)

    remove_overlapping_locs = property(
        get_remove_overlapping_locs, set_remove_overlapping_locs,
        doc=('If minor ticker locations that overlap with major '
             'ticker locations should be trimmed.'))

    def set_label_coords(self, x, y, transform=None):
        """
        Set the coordinates of the label.

        By default, the x coordinate of the y label and the y coordinate of the
        x label are determined by the tick label bounding boxes, but this can
        lead to poor alignment of multiple labels if there are multiple axes.

        You can also specify the coordinate system of the label with the
        transform.  If None, the default coordinate system will be the axes
        coordinate system: (0, 0) is bottom left, (0.5, 0.5) is center, etc.
        """
        self._autolabelpos = False
        if transform is None:
            transform = self.axes.transAxes

        self.label.set_transform(transform)
        self.label.set_position((x, y))
        self.stale = True

    def get_transform(self):
        return self._scale.get_transform()

    def get_scale(self):
        """Return this Axis' scale (as a str)."""
        return self._scale.name

    def _set_scale(self, value, **kwargs):
        if not isinstance(value, mscale.ScaleBase):
            self._scale = mscale.scale_factory(value, self, **kwargs)
        else:
            self._scale = value
        self._scale.set_default_locators_and_formatters(self)

        self.isDefault_majloc = True
        self.isDefault_minloc = True
        self.isDefault_majfmt = True
        self.isDefault_minfmt = True

    def limit_range_for_scale(self, vmin, vmax):
        return self._scale.limit_range_for_scale(vmin, vmax, self.get_minpos())

    def get_children(self):
        return [self.label, self.offsetText,
                *self.get_major_ticks(), *self.get_minor_ticks()]

    def _reset_major_tick_kw(self):
        self._major_tick_kw.clear()
        self._major_tick_kw['gridOn'] = (
                mpl.rcParams['axes.grid'] and
                mpl.rcParams['axes.grid.which'] in ('both', 'major'))

    def _reset_minor_tick_kw(self):
        self._minor_tick_kw.clear()
        self._minor_tick_kw['gridOn'] = (
                mpl.rcParams['axes.grid'] and
                mpl.rcParams['axes.grid.which'] in ('both', 'minor'))

    def clear(self):
        """
        Clear the axis.

        This resets axis properties to their default values:

        - the label
        - the scale
        - locators, formatters and ticks
        - major and minor grid
        - units
        - registered callbacks
        """

        self.label.set_text('')  # self.set_label_text would change isDefault_

        self._set_scale('linear')

        # Clear the callback registry for this axis, or it may "leak"
        self.callbacks = cbook.CallbackRegistry()

        # whether the grids are on
        self._major_tick_kw['gridOn'] = (
                mpl.rcParams['axes.grid'] and
                mpl.rcParams['axes.grid.which'] in ('both', 'major'))
        self._minor_tick_kw['gridOn'] = (
                mpl.rcParams['axes.grid'] and
                mpl.rcParams['axes.grid.which'] in ('both', 'minor'))
        self.reset_ticks()

        self.converter = None
        self.units = None
        self.set_units(None)
        self.stale = True

    @_api.deprecated("3.4", alternative="Axis.clear()")
    def cla(self):
        """Clear this axis."""
        return self.clear()

    def reset_ticks(self):
        """
        Re-initialize the major and minor Tick lists.

        Each list starts with a single fresh Tick.
        """
        # Restore the lazy tick lists.
        try:
            del self.majorTicks
        except AttributeError:
            pass
        try:
            del self.minorTicks
        except AttributeError:
            pass
        try:
            self.set_clip_path(self.axes.patch)
        except AttributeError:
            pass

    def set_tick_params(self, which='major', reset=False, **kw):
        """
        Set appearance parameters for ticks, ticklabels, and gridlines.

        For documentation of keyword arguments, see
        :meth:`matplotlib.axes.Axes.tick_params`.
        """
        _api.check_in_list(['major', 'minor', 'both'], which=which)
        kwtrans = self._translate_tick_kw(kw)

        # the kwargs are stored in self._major/minor_tick_kw so that any
        # future new ticks will automatically get them
        if reset:
            if which in ['major', 'both']:
                self._reset_major_tick_kw()
                self._major_tick_kw.update(kwtrans)
            if which in ['minor', 'both']:
                self._reset_minor_tick_kw()
                self._minor_tick_kw.update(kwtrans)
            self.reset_ticks()
        else:
            if which in ['major', 'both']:
                self._major_tick_kw.update(kwtrans)
                for tick in self.majorTicks:
                    tick._apply_params(**kwtrans)
            if which in ['minor', 'both']:
                self._minor_tick_kw.update(kwtrans)
                for tick in self.minorTicks:
                    tick._apply_params(**kwtrans)
            # labelOn and labelcolor also apply to the offset text.
            if 'label1On' in kwtrans or 'label2On' in kwtrans:
                self.offsetText.set_visible(
                    self._major_tick_kw.get('label1On', False)
                    or self._major_tick_kw.get('label2On', False))
            if 'labelcolor' in kwtrans:
                self.offsetText.set_color(kwtrans['labelcolor'])

        self.stale = True

    @staticmethod
    def _translate_tick_kw(kw):
        # The following lists may be moved to a more accessible location.
        kwkeys = ['size', 'width', 'color', 'tickdir', 'pad',
                  'labelsize', 'labelcolor', 'zorder', 'gridOn',
                  'tick1On', 'tick2On', 'label1On', 'label2On',
                  'length', 'direction', 'left', 'bottom', 'right', 'top',
                  'labelleft', 'labelbottom', 'labelright', 'labeltop',
                  'labelrotation'] + _gridline_param_names
        kwtrans = {}
        if 'length' in kw:
            kwtrans['size'] = kw.pop('length')
        if 'direction' in kw:
            kwtrans['tickdir'] = kw.pop('direction')
        if 'rotation' in kw:
            kwtrans['labelrotation'] = kw.pop('rotation')
        if 'left' in kw:
            kwtrans['tick1On'] = kw.pop('left')
        if 'bottom' in kw:
            kwtrans['tick1On'] = kw.pop('bottom')
        if 'right' in kw:
            kwtrans['tick2On'] = kw.pop('right')
        if 'top' in kw:
            kwtrans['tick2On'] = kw.pop('top')
        if 'labelleft' in kw:
            kwtrans['label1On'] = kw.pop('labelleft')
        if 'labelbottom' in kw:
            kwtrans['label1On'] = kw.pop('labelbottom')
        if 'labelright' in kw:
            kwtrans['label2On'] = kw.pop('labelright')
        if 'labeltop' in kw:
            kwtrans['label2On'] = kw.pop('labeltop')
        if 'colors' in kw:
            c = kw.pop('colors')
            kwtrans['color'] = c
            kwtrans['labelcolor'] = c
        # Maybe move the checking up to the caller of this method.
        for key in kw:
            if key not in kwkeys:
                raise ValueError(
                    "keyword %s is not recognized; valid keywords are %s"
                    % (key, kwkeys))
        kwtrans.update(kw)
        return kwtrans

    def set_clip_path(self, clippath, transform=None):
        super().set_clip_path(clippath, transform)
        for child in self.majorTicks + self.minorTicks:
            child.set_clip_path(clippath, transform)
        self.stale = True

    def get_view_interval(self):
        """Return the ``(min, max)`` view limits of this axis."""
        raise NotImplementedError('Derived must override')

    def set_view_interval(self, vmin, vmax, ignore=False):
        """
        Set the axis view limits.  This method is for internal use; Matplotlib
        users should typically use e.g. `~.Axes.set_xlim` or `~.Axes.set_ylim`.

        If *ignore* is False (the default), this method will never reduce the
        preexisting view limits, only expand them if *vmin* or *vmax* are not
        within them.  Moreover, the order of *vmin* and *vmax* does not matter;
        the orientation of the axis will not change.

        If *ignore* is True, the view limits will be set exactly to ``(vmin,
        vmax)`` in that order.
        """
        raise NotImplementedError('Derived must override')

    def get_data_interval(self):
        """Return the ``(min, max)`` data limits of this axis."""
        raise NotImplementedError('Derived must override')

    def set_data_interval(self, vmin, vmax, ignore=False):
        """
        Set the axis data limits.  This method is for internal use.

        If *ignore* is False (the default), this method will never reduce the
        preexisting data limits, only expand them if *vmin* or *vmax* are not
        within them.  Moreover, the order of *vmin* and *vmax* does not matter;
        the orientation of the axis will not change.

        If *ignore* is True, the data limits will be set exactly to ``(vmin,
        vmax)`` in that order.
        """
        raise NotImplementedError('Derived must override')

    def get_inverted(self):
        """
        Return whether this Axis is oriented in the "inverse" direction.

        The "normal" direction is increasing to the right for the x-axis and to
        the top for the y-axis; the "inverse" direction is increasing to the
        left for the x-axis and to the bottom for the y-axis.
        """
        low, high = self.get_view_interval()
        return high < low

    def set_inverted(self, inverted):
        """
        Set whether this Axis is oriented in the "inverse" direction.

        The "normal" direction is increasing to the right for the x-axis and to
        the top for the y-axis; the "inverse" direction is increasing to the
        left for the x-axis and to the bottom for the y-axis.
        """
        # Currently, must be implemented in subclasses using set_xlim/set_ylim
        # rather than generically using set_view_interval, so that shared
        # axes get updated as well.
        raise NotImplementedError('Derived must override')

    def set_default_intervals(self):
        """
        Set the default limits for the axis data and view interval if they
        have not been not mutated yet.
        """
        # this is mainly in support of custom object plotting.  For
        # example, if someone passes in a datetime object, we do not
        # know automagically how to set the default min/max of the
        # data and view limits.  The unit conversion AxisInfo
        # interface provides a hook for custom types to register
        # default limits through the AxisInfo.default_limits
        # attribute, and the derived code below will check for that
        # and use it if it's available (else just use 0..1)

    def _set_artist_props(self, a):
        if a is None:
            return
        a.set_figure(self.figure)

    def get_ticklabel_extents(self, renderer):
        """
        Get the extents of the tick labels on either side
        of the axes.
        """

        ticks_to_draw = self._update_ticks()
        ticklabelBoxes, ticklabelBoxes2 = self._get_tick_bboxes(ticks_to_draw,
                                                                renderer)

        if len(ticklabelBoxes):
            bbox = mtransforms.Bbox.union(ticklabelBoxes)
        else:
            bbox = mtransforms.Bbox.from_extents(0, 0, 0, 0)
        if len(ticklabelBoxes2):
            bbox2 = mtransforms.Bbox.union(ticklabelBoxes2)
        else:
            bbox2 = mtransforms.Bbox.from_extents(0, 0, 0, 0)
        return bbox, bbox2

    def _update_ticks(self):
        """
        Update ticks (position and labels) using the current data interval of
        the axes.  Return the list of ticks that will be drawn.
        """
        major_locs = self.get_majorticklocs()
        major_labels = self.major.formatter.format_ticks(major_locs)
        major_ticks = self.get_major_ticks(len(major_locs))
        self.major.formatter.set_locs(major_locs)
        for tick, loc, label in zip(major_ticks, major_locs, major_labels):
            tick.update_position(loc)
            tick.set_label1(label)
            tick.set_label2(label)
        minor_locs = self.get_minorticklocs()
        minor_labels = self.minor.formatter.format_ticks(minor_locs)
        minor_ticks = self.get_minor_ticks(len(minor_locs))
        self.minor.formatter.set_locs(minor_locs)
        for tick, loc, label in zip(minor_ticks, minor_locs, minor_labels):
            tick.update_position(loc)
            tick.set_label1(label)
            tick.set_label2(label)
        ticks = [*major_ticks, *minor_ticks]

        view_low, view_high = self.get_view_interval()
        if view_low > view_high:
            view_low, view_high = view_high, view_low

        interval_t = self.get_transform().transform([view_low, view_high])

        ticks_to_draw = []
        for tick in ticks:
            try:
                loc_t = self.get_transform().transform(tick.get_loc())
            except AssertionError:
                # transforms.transform doesn't allow masked values but
                # some scales might make them, so we need this try/except.
                pass
            else:
                if mtransforms._interval_contains_close(interval_t, loc_t):
                    ticks_to_draw.append(tick)

        return ticks_to_draw

    def _get_tick_bboxes(self, ticks, renderer):
        """Return lists of bboxes for ticks' label1's and label2's."""
        return ([tick.label1.get_window_extent(renderer)
                 for tick in ticks if tick.label1.get_visible()],
                [tick.label2.get_window_extent(renderer)
                 for tick in ticks if tick.label2.get_visible()])

    def get_tightbbox(self, renderer, *, for_layout_only=False):
        """
        Return a bounding box that encloses the axis. It only accounts
        tick labels, axis label, and offsetText.

        If *for_layout_only* is True, then the width of the label (if this
        is an x-axis) or the height of the label (if this is a y-axis) is
        collapsed to near zero.  This allows tight/constrained_layout to ignore
        too-long labels when doing their layout.
        """
        if not self.get_visible():
            return

        ticks_to_draw = self._update_ticks()

        self._update_label_position(renderer)

        # go back to just this axis's tick labels
        ticklabelBoxes, ticklabelBoxes2 = self._get_tick_bboxes(
                    ticks_to_draw, renderer)

        self._update_offset_text_position(ticklabelBoxes, ticklabelBoxes2)
        self.offsetText.set_text(self.major.formatter.get_offset())

        bboxes = [
            *(a.get_window_extent(renderer)
              for a in [self.offsetText]
              if a.get_visible()),
            *ticklabelBoxes,
            *ticklabelBoxes2,
        ]
        # take care of label
        if self.label.get_visible():
            bb = self.label.get_window_extent(renderer)
            # for constrained/tight_layout, we want to ignore the label's
            # width/height because the adjustments they make can't be improved.
            # this code collapses the relevant direction
            if for_layout_only:
                if self.axis_name == "x" and bb.width > 0:
                    bb.x0 = (bb.x0 + bb.x1) / 2 - 0.5
                    bb.x1 = bb.x0 + 1.0
                if self.axis_name == "y" and bb.height > 0:
                    bb.y0 = (bb.y0 + bb.y1) / 2 - 0.5
                    bb.y1 = bb.y0 + 1.0
            bboxes.append(bb)
        bboxes = [b for b in bboxes
                  if 0 < b.width < np.inf and 0 < b.height < np.inf]
        if bboxes:
            return mtransforms.Bbox.union(bboxes)
        else:
            return None

    def get_tick_padding(self):
        values = []
        if len(self.majorTicks):
            values.append(self.majorTicks[0].get_tick_padding())
        if len(self.minorTicks):
            values.append(self.minorTicks[0].get_tick_padding())
        return max(values, default=0)

    @martist.allow_rasterization
    def draw(self, renderer, *args, **kwargs):
        # docstring inherited

        if not self.get_visible():
            return
        renderer.open_group(__name__, gid=self.get_gid())

        ticks_to_draw = self._update_ticks()
        ticklabelBoxes, ticklabelBoxes2 = self._get_tick_bboxes(ticks_to_draw,
                                                                renderer)

        for tick in ticks_to_draw:
            tick.draw(renderer)

        # scale up the axis label box to also find the neighbors, not
        # just the tick labels that actually overlap note we need a
        # *copy* of the axis label box because we don't want to scale
        # the actual bbox

        self._update_label_position(renderer)

        self.label.draw(renderer)

        self._update_offset_text_position(ticklabelBoxes, ticklabelBoxes2)
        self.offsetText.set_text(self.major.formatter.get_offset())
        self.offsetText.draw(renderer)

        renderer.close_group(__name__)
        self.stale = False

    def get_gridlines(self):
        r"""Return this Axis' grid lines as a list of `.Line2D`\s."""
        ticks = self.get_major_ticks()
        return cbook.silent_list('Line2D gridline',
                                 [tick.gridline for tick in ticks])

    def get_label(self):
        """Return the axis label as a Text instance."""
        return self.label

    def get_offset_text(self):
        """Return the axis offsetText as a Text instance."""
        return self.offsetText

    def get_pickradius(self):
        """Return the depth of the axis used by the picker."""
        return self.pickradius

    def get_majorticklabels(self):
        """Return this Axis' major tick labels, as a list of `~.text.Text`."""
        ticks = self.get_major_ticks()
        labels1 = [tick.label1 for tick in ticks if tick.label1.get_visible()]
        labels2 = [tick.label2 for tick in ticks if tick.label2.get_visible()]
        return labels1 + labels2

    def get_minorticklabels(self):
        """Return this Axis' minor tick labels, as a list of `~.text.Text`."""
        ticks = self.get_minor_ticks()
        labels1 = [tick.label1 for tick in ticks if tick.label1.get_visible()]
        labels2 = [tick.label2 for tick in ticks if tick.label2.get_visible()]
        return labels1 + labels2

    def get_ticklabels(self, minor=False, which=None):
        """
        Get this Axis' tick labels.

        Parameters
        ----------
        minor : bool
           Whether to return the minor or the major ticklabels.

        which : None, ('minor', 'major', 'both')
           Overrides *minor*.

           Selects which ticklabels to return

        Returns
        -------
        list of `~matplotlib.text.Text`

        Notes
        -----
        The tick label strings are not populated until a ``draw`` method has
        been called.

        See also: `~.pyplot.draw` and `~.FigureCanvasBase.draw`.
        """
        if which is not None:
            if which == 'minor':
                return self.get_minorticklabels()
            elif which == 'major':
                return self.get_majorticklabels()
            elif which == 'both':
                return self.get_majorticklabels() + self.get_minorticklabels()
            else:
                _api.check_in_list(['major', 'minor', 'both'], which=which)
        if minor:
            return self.get_minorticklabels()
        return self.get_majorticklabels()

    def get_majorticklines(self):
        r"""Return this Axis' major tick lines as a list of `.Line2D`\s."""
        lines = []
        ticks = self.get_major_ticks()
        for tick in ticks:
            lines.append(tick.tick1line)
            lines.append(tick.tick2line)
        return cbook.silent_list('Line2D ticklines', lines)

    def get_minorticklines(self):
        r"""Return this Axis' minor tick lines as a list of `.Line2D`\s."""
        lines = []
        ticks = self.get_minor_ticks()
        for tick in ticks:
            lines.append(tick.tick1line)
            lines.append(tick.tick2line)
        return cbook.silent_list('Line2D ticklines', lines)

    def get_ticklines(self, minor=False):
        r"""Return this Axis' tick lines as a list of `.Line2D`\s."""
        if minor:
            return self.get_minorticklines()
        return self.get_majorticklines()

    def get_majorticklocs(self):
        """Return this Axis' major tick locations in data coordinates."""
        return self.major.locator()

    def get_minorticklocs(self):
        """Return this Axis' minor tick locations in data coordinates."""
        # Remove minor ticks duplicating major ticks.
        major_locs = self.major.locator()
        minor_locs = self.minor.locator()
        transform = self._scale.get_transform()
        tr_minor_locs = transform.transform(minor_locs)
        tr_major_locs = transform.transform(major_locs)
        lo, hi = sorted(transform.transform(self.get_view_interval()))
        # Use the transformed view limits as scale.  1e-5 is the default rtol
        # for np.isclose.
        tol = (hi - lo) * 1e-5
        if self.remove_overlapping_locs:
            minor_locs = [
                loc for loc, tr_loc in zip(minor_locs, tr_minor_locs)
                if ~np.isclose(tr_loc, tr_major_locs, atol=tol, rtol=0).any()]
        return minor_locs

    def get_ticklocs(self, *, minor=False):
        """Return this Axis' tick locations in data coordinates."""
        return self.get_minorticklocs() if minor else self.get_majorticklocs()

    def get_ticks_direction(self, minor=False):
        """
        Get the tick directions as a numpy array

        Parameters
        ----------
        minor : bool, default: False
            True to return the minor tick directions,
            False to return the major tick directions.

        Returns
        -------
        numpy array of tick directions
        """
        if minor:
            return np.array(
                [tick._tickdir for tick in self.get_minor_ticks()])
        else:
            return np.array(
                [tick._tickdir for tick in self.get_major_ticks()])

    def _get_tick(self, major):
        """Return the default tick instance."""
        raise NotImplementedError('derived must override')

    def _get_tick_label_size(self, axis_name):
        """
        Return the text size of tick labels for this Axis.

        This is a convenience function to avoid having to create a `Tick` in
        `.get_tick_space`, since it is expensive.
        """
        tick_kw = self._major_tick_kw
        size = tick_kw.get('labelsize',
                           mpl.rcParams[f'{axis_name}tick.labelsize'])
        return mtext.FontProperties(size=size).get_size_in_points()

    def _copy_tick_props(self, src, dest):
        """Copy the properties from *src* tick to *dest* tick."""
        if src is None or dest is None:
            return
        dest.label1.update_from(src.label1)
        dest.label2.update_from(src.label2)
        dest.tick1line.update_from(src.tick1line)
        dest.tick2line.update_from(src.tick2line)
        dest.gridline.update_from(src.gridline)

    def get_label_text(self):
        """Get the text of the label."""
        return self.label.get_text()

    def get_major_locator(self):
        """Get the locator of the major ticker."""
        return self.major.locator

    def get_minor_locator(self):
        """Get the locator of the minor ticker."""
        return self.minor.locator

    def get_major_formatter(self):
        """Get the formatter of the major ticker."""
        return self.major.formatter

    def get_minor_formatter(self):
        """Get the formatter of the minor ticker."""
        return self.minor.formatter

    def get_major_ticks(self, numticks=None):
        r"""Return the list of major `.Tick`\s."""
        if numticks is None:
            numticks = len(self.get_majorticklocs())

        while len(self.majorTicks) < numticks:
            # Update the new tick label properties from the old.
            tick = self._get_tick(major=True)
            self.majorTicks.append(tick)
            self._copy_tick_props(self.majorTicks[0], tick)

        return self.majorTicks[:numticks]

    def get_minor_ticks(self, numticks=None):
        r"""Return the list of minor `.Tick`\s."""
        if numticks is None:
            numticks = len(self.get_minorticklocs())

        while len(self.minorTicks) < numticks:
            # Update the new tick label properties from the old.
            tick = self._get_tick(major=False)
            self.minorTicks.append(tick)
            self._copy_tick_props(self.minorTicks[0], tick)

        return self.minorTicks[:numticks]

    @_api.rename_parameter("3.5", "b", "visible")
    def grid(self, visible=None, which='major', **kwargs):
        """
        Configure the grid lines.

        Parameters
        ----------
        visible : bool or None
            Whether to show the grid lines.  If any *kwargs* are supplied, it
            is assumed you want the grid on and *visible* will be set to True.

            If *visible* is *None* and there are no *kwargs*, this toggles the
            visibility of the lines.

        which : {'major', 'minor', 'both'}
            The grid lines to apply the changes on.

        **kwargs : `.Line2D` properties
            Define the line properties of the grid, e.g.::

                grid(color='r', linestyle='-', linewidth=2)
        """
        if kwargs:
            if visible is None:
                visible = True
            elif not visible:  # something false-like but not None
                _api.warn_external('First parameter to grid() is false, '
                                   'but line properties are supplied. The '
                                   'grid will be enabled.')
                visible = True
        which = which.lower()
        _api.check_in_list(['major', 'minor', 'both'], which=which)
        gridkw = {'grid_' + item[0]: item[1] for item in kwargs.items()}
        if which in ['minor', 'both']:
            gridkw['gridOn'] = (not self._minor_tick_kw['gridOn']
                                if visible is None else visible)
            self.set_tick_params(which='minor', **gridkw)
        if which in ['major', 'both']:
            gridkw['gridOn'] = (not self._major_tick_kw['gridOn']
                                if visible is None else visible)
            self.set_tick_params(which='major', **gridkw)
        self.stale = True

    def update_units(self, data):
        """
        Introspect *data* for units converter and update the
        axis.converter instance if necessary. Return *True*
        if *data* is registered for unit conversion.
        """
        converter = munits.registry.get_converter(data)
        if converter is None:
            return False

        neednew = self.converter != converter
        self.converter = converter
        default = self.converter.default_units(data, self)
        if default is not None and self.units is None:
            self.set_units(default)

        elif neednew:
            self._update_axisinfo()
        self.stale = True
        return True

    def _update_axisinfo(self):
        """
        Check the axis converter for the stored units to see if the
        axis info needs to be updated.
        """
        if self.converter is None:
            return

        info = self.converter.axisinfo(self.units, self)

        if info is None:
            return
        if info.majloc is not None and \
           self.major.locator != info.majloc and self.isDefault_majloc:
            self.set_major_locator(info.majloc)
            self.isDefault_majloc = True
        if info.minloc is not None and \
           self.minor.locator != info.minloc and self.isDefault_minloc:
            self.set_minor_locator(info.minloc)
            self.isDefault_minloc = True
        if info.majfmt is not None and \
           self.major.formatter != info.majfmt and self.isDefault_majfmt:
            self.set_major_formatter(info.majfmt)
            self.isDefault_majfmt = True
        if info.minfmt is not None and \
           self.minor.formatter != info.minfmt and self.isDefault_minfmt:
            self.set_minor_formatter(info.minfmt)
            self.isDefault_minfmt = True
        if info.label is not None and self.isDefault_label:
            self.set_label_text(info.label)
            self.isDefault_label = True

        self.set_default_intervals()

    def have_units(self):
        return self.converter is not None or self.units is not None

    def convert_units(self, x):
        # If x is natively supported by Matplotlib, doesn't need converting
        if munits._is_natively_supported(x):
            return x

        if self.converter is None:
            self.converter = munits.registry.get_converter(x)

        if self.converter is None:
            return x
        try:
            ret = self.converter.convert(x, self.units, self)
        except Exception as e:
            raise munits.ConversionError('Failed to convert value(s) to axis '
                                         f'units: {x!r}') from e
        return ret

    def set_units(self, u):
        """
        Set the units for axis.

        Parameters
        ----------
        u : units tag

        Notes
        -----
        The units of any shared axis will also be updated.
        """
        if u == self.units:
            return
        for name, axis in self.axes._get_axis_map().items():
            if self is axis:
                shared = [
                    getattr(ax, f"{name}axis")
                    for ax
                    in self.axes._shared_axes[name].get_siblings(self.axes)]
                break
        else:
            shared = [self]
        for axis in shared:
            axis.units = u
            axis._update_axisinfo()
            axis.callbacks.process('units')
            axis.callbacks.process('units finalize')
            axis.stale = True

    def get_units(self):
        """Return the units for axis."""
        return self.units

    def set_label_text(self, label, fontdict=None, **kwargs):
        """
        Set the text value of the axis label.

        Parameters
        ----------
        label : str
            Text string.
        fontdict : dict
            Text properties.
        **kwargs
            Merged into fontdict.
        """
        self.isDefault_label = False
        self.label.set_text(label)
        if fontdict is not None:
            self.label.update(fontdict)
        self.label.update(kwargs)
        self.stale = True
        return self.label

    def set_major_formatter(self, formatter):
        """
        Set the formatter of the major ticker.

        In addition to a `~matplotlib.ticker.Formatter` instance,
        this also accepts a ``str`` or function.

        For a ``str`` a `~matplotlib.ticker.StrMethodFormatter` is used.
        The field used for the value must be labeled ``'x'`` and the field used
        for the position must be labeled ``'pos'``.
        See the  `~matplotlib.ticker.StrMethodFormatter` documentation for
        more information.

        For a function, a `~matplotlib.ticker.FuncFormatter` is used.
        The function must take two inputs (a tick value ``x`` and a
        position ``pos``), and return a string containing the corresponding
        tick label.
        See the  `~matplotlib.ticker.FuncFormatter` documentation for
        more information.

        Parameters
        ----------
        formatter : `~matplotlib.ticker.Formatter`, ``str``, or function
        """
        self._set_formatter(formatter, self.major)

    def set_minor_formatter(self, formatter):
        """
        Set the formatter of the minor ticker.

        In addition to a `~matplotlib.ticker.Formatter` instance,
        this also accepts a ``str`` or function.
        See `.Axis.set_major_formatter` for more information.

        Parameters
        ----------
        formatter : `~matplotlib.ticker.Formatter`, ``str``, or function
        """
        self._set_formatter(formatter, self.minor)

    def _set_formatter(self, formatter, level):
        if isinstance(formatter, str):
            formatter = mticker.StrMethodFormatter(formatter)
        # Don't allow any other TickHelper to avoid easy-to-make errors,
        # like using a Locator instead of a Formatter.
        elif (callable(formatter) and
              not isinstance(formatter, mticker.TickHelper)):
            formatter = mticker.FuncFormatter(formatter)
        else:
            _api.check_isinstance(mticker.Formatter, formatter=formatter)

        if (isinstance(formatter, mticker.FixedFormatter)
                and len(formatter.seq) > 0
                and not isinstance(level.locator, mticker.FixedLocator)):
            _api.warn_external('FixedFormatter should only be used together '
                               'with FixedLocator')

        if level == self.major:
            self.isDefault_majfmt = False
        else:
            self.isDefault_minfmt = False

        level.formatter = formatter
        formatter.set_axis(self)
        self.stale = True

    def set_major_locator(self, locator):
        """
        Set the locator of the major ticker.

        Parameters
        ----------
        locator : `~matplotlib.ticker.Locator`
        """
        _api.check_isinstance(mticker.Locator, locator=locator)
        self.isDefault_majloc = False
        self.major.locator = locator
        if self.major.formatter:
            self.major.formatter._set_locator(locator)
        locator.set_axis(self)
        self.stale = True

    def set_minor_locator(self, locator):
        """
        Set the locator of the minor ticker.

        Parameters
        ----------
        locator : `~matplotlib.ticker.Locator`
        """
        _api.check_isinstance(mticker.Locator, locator=locator)
        self.isDefault_minloc = False
        self.minor.locator = locator
        if self.minor.formatter:
            self.minor.formatter._set_locator(locator)
        locator.set_axis(self)
        self.stale = True

    def set_pickradius(self, pickradius):
        """
        Set the depth of the axis used by the picker.

        Parameters
        ----------
        pickradius :  float
        """
        self.pickradius = pickradius

    # Helper for set_ticklabels. Defining it here makes it pickleable.
    @staticmethod
    def _format_with_dict(tickd, x, pos):
        return tickd.get(x, "")

    def set_ticklabels(self, ticklabels, *, minor=False, **kwargs):
        r"""
        Set the text values of the tick labels.

        .. admonition:: Discouraged

            The use of this method is discouraged, because of the dependency
            on tick positions. In most cases, you'll want to use
            ``set_[x/y]ticks(positions, labels)`` instead.

            If you are using this method, you should always fix the tick
            positions before, e.g. by using `.Axis.set_ticks` or by explicitly
            setting a `~.ticker.FixedLocator`. Otherwise, ticks are free to
            move and the labels may end up in unexpected positions.

        Parameters
        ----------
        ticklabels : sequence of str or of `.Text`\s
            Texts for labeling each tick location in the sequence set by
            `.Axis.set_ticks`; the number of labels must match the number of
            locations.
        minor : bool
            If True, set minor ticks instead of major ticks.
        **kwargs
            Text properties.

        Returns
        -------
        list of `.Text`\s
            For each tick, includes ``tick.label1`` if it is visible, then
            ``tick.label2`` if it is visible, in that order.
        """
        ticklabels = [t.get_text() if hasattr(t, 'get_text') else t
                      for t in ticklabels]
        locator = (self.get_minor_locator() if minor
                   else self.get_major_locator())
        if isinstance(locator, mticker.FixedLocator):
            # Passing [] as a list of ticklabels is often used as a way to
            # remove all tick labels, so only error for > 0 ticklabels
            if len(locator.locs) != len(ticklabels) and len(ticklabels) != 0:
                raise ValueError(
                    "The number of FixedLocator locations"
                    f" ({len(locator.locs)}), usually from a call to"
                    " set_ticks, does not match"
                    f" the number of ticklabels ({len(ticklabels)}).")
            tickd = {loc: lab for loc, lab in zip(locator.locs, ticklabels)}
            func = functools.partial(self._format_with_dict, tickd)
            formatter = mticker.FuncFormatter(func)
        else:
            formatter = mticker.FixedFormatter(ticklabels)

        if minor:
            self.set_minor_formatter(formatter)
            locs = self.get_minorticklocs()
            ticks = self.get_minor_ticks(len(locs))
        else:
            self.set_major_formatter(formatter)
            locs = self.get_majorticklocs()
            ticks = self.get_major_ticks(len(locs))

        ret = []
        for pos, (loc, tick) in enumerate(zip(locs, ticks)):
            tick.update_position(loc)
            tick_label = formatter(loc, pos)
            # deal with label1
            tick.label1.set_text(tick_label)
            tick.label1.update(kwargs)
            # deal with label2
            tick.label2.set_text(tick_label)
            tick.label2.update(kwargs)
            # only return visible tick labels
            if tick.label1.get_visible():
                ret.append(tick.label1)
            if tick.label2.get_visible():
                ret.append(tick.label2)

        self.stale = True
        return ret

    # Wrapper around set_ticklabels used to generate Axes.set_x/ytickabels; can
    # go away once the API of Axes.set_x/yticklabels becomes consistent.
    def _set_ticklabels(self, labels, *, fontdict=None, minor=False, **kwargs):
        """
        Set this Axis' labels with list of string labels.

        .. warning::
            This method should only be used after fixing the tick positions
            using `.Axis.set_ticks`. Otherwise, the labels may end up in
            unexpected positions.

        Parameters
        ----------
        labels : list of str
            The label texts.

        fontdict : dict, optional
            A dictionary controlling the appearance of the ticklabels.
            The default *fontdict* is::

               {'fontsize': rcParams['axes.titlesize'],
                'fontweight': rcParams['axes.titleweight'],
                'verticalalignment': 'baseline',
                'horizontalalignment': loc}

        minor : bool, default: False
            Whether to set the minor ticklabels rather than the major ones.

        Returns
        -------
        list of `.Text`
            The labels.

        Other Parameters
        ----------------
        **kwargs : `~.text.Text` properties.
        """
        if fontdict is not None:
            kwargs.update(fontdict)
        return self.set_ticklabels(labels, minor=minor, **kwargs)

    def _set_tick_locations(self, ticks, *, minor=False):
        # see docstring of set_ticks

        # XXX if the user changes units, the information will be lost here
        ticks = self.convert_units(ticks)
        for name, axis in self.axes._get_axis_map().items():
            if self is axis:
                shared = [
                    getattr(ax, f"{name}axis")
                    for ax
                    in self.axes._shared_axes[name].get_siblings(self.axes)]
                break
        else:
            shared = [self]
        for axis in shared:
            if len(ticks) > 1:
                xleft, xright = axis.get_view_interval()
                if xright > xleft:
                    axis.set_view_interval(min(ticks), max(ticks))
                else:
                    axis.set_view_interval(max(ticks), min(ticks))
        self.axes.stale = True
        if minor:
            self.set_minor_locator(mticker.FixedLocator(ticks))
            return self.get_minor_ticks(len(ticks))
        else:
            self.set_major_locator(mticker.FixedLocator(ticks))
            return self.get_major_ticks(len(ticks))

    def set_ticks(self, ticks, labels=None, *, minor=False, **kwargs):
        """
        Set this Axis' tick locations and optionally labels.

        If necessary, the view limits of the Axis are expanded so that all
        given ticks are visible.

        Parameters
        ----------
        ticks : list of floats
            List of tick locations.
        labels : list of str, optional
            List of tick labels. If not set, the labels show the data value.
        minor : bool, default: False
            If ``False``, set the major ticks; if ``True``, the minor ticks.
        **kwargs
            `.Text` properties for the labels. These take effect only if you
            pass *labels*. In other cases, please use `~.Axes.tick_params`.

        Notes
        -----
        The mandatory expansion of the view limits is an intentional design
        choice to prevent the surprise of a non-visible tick. If you need
        other limits, you should set the limits explicitly after setting the
        ticks.
        """
        result = self._set_tick_locations(ticks, minor=minor)
        if labels is not None:
            self.set_ticklabels(labels, minor=minor, **kwargs)
        return result

    def _get_tick_boxes_siblings(self, renderer):
        """
        Get the bounding boxes for this `.axis` and its siblings
        as set by `.Figure.align_xlabels` or  `.Figure.align_ylabels`.

        By default it just gets bboxes for self.
        """
        # Get the Grouper keeping track of x or y label groups for this figure.
        axis_names = [
            name for name, axis in self.axes._get_axis_map().items()
            if name in self.figure._align_label_groups and axis is self]
        if len(axis_names) != 1:
            return [], []
        axis_name, = axis_names
        grouper = self.figure._align_label_groups[axis_name]
        bboxes = []
        bboxes2 = []
        # If we want to align labels from other axes:
        for ax in grouper.get_siblings(self.axes):
            axis = getattr(ax, f"{axis_name}axis")
            ticks_to_draw = axis._update_ticks()
            tlb, tlb2 = axis._get_tick_bboxes(ticks_to_draw, renderer)
            bboxes.extend(tlb)
            bboxes2.extend(tlb2)
        return bboxes, bboxes2

    def _update_label_position(self, renderer):
        """
        Update the label position based on the bounding box enclosing
        all the ticklabels and axis spine.
        """
        raise NotImplementedError('Derived must override')

    def _update_offset_text_position(self, bboxes, bboxes2):
        """
        Update the offset text position based on the sequence of bounding
        boxes of all the ticklabels.
        """
        raise NotImplementedError('Derived must override')

    def axis_date(self, tz=None):
        """
        Set up axis ticks and labels to treat data along this Axis as dates.

        Parameters
        ----------
        tz : str or `datetime.tzinfo`, default: :rc:`timezone`
            The timezone used to create date labels.
        """
        # By providing a sample datetime instance with the desired timezone,
        # the registered converter can be selected, and the "units" attribute,
        # which is the timezone, can be set.
        if isinstance(tz, str):
            import dateutil.tz
            tz = dateutil.tz.gettz(tz)
        self.update_units(datetime.datetime(2009, 1, 1, 0, 0, 0, 0, tz))

    def get_tick_space(self):
        """Return the estimated number of ticks that can fit on the axis."""
        # Must be overridden in the subclass
        raise NotImplementedError()

    def _get_ticks_position(self):
        """
        Helper for `XAxis.get_ticks_position` and `YAxis.get_ticks_position`.

        Check the visibility of tick1line, label1, tick2line, and label2 on
        the first major and the first minor ticks, and return

        - 1 if only tick1line and label1 are visible (which corresponds to
          "bottom" for the x-axis and "left" for the y-axis);
        - 2 if only tick2line and label2 are visible (which corresponds to
          "top" for the x-axis and "right" for the y-axis);
        - "default" if only tick1line, tick2line and label1 are visible;
        - "unknown" otherwise.
        """
        major = self.majorTicks[0]
        minor = self.minorTicks[0]
        if all(tick.tick1line.get_visible()
               and not tick.tick2line.get_visible()
               and tick.label1.get_visible()
               and not tick.label2.get_visible()
               for tick in [major, minor]):
            return 1
        elif all(tick.tick2line.get_visible()
                 and not tick.tick1line.get_visible()
                 and tick.label2.get_visible()
                 and not tick.label1.get_visible()
                 for tick in [major, minor]):
            return 2
        elif all(tick.tick1line.get_visible()
                 and tick.tick2line.get_visible()
                 and tick.label1.get_visible()
                 and not tick.label2.get_visible()
                 for tick in [major, minor]):
            return "default"
        else:
            return "unknown"

    def get_label_position(self):
        """
        Return the label position (top or bottom)
        """
        return self.label_position

    def set_label_position(self, position):
        """
        Set the label position (top or bottom)

        Parameters
        ----------
        position : {'top', 'bottom'}
        """
        raise NotImplementedError()

    def get_minpos(self):
        raise NotImplementedError()
