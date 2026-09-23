class YAxis(Axis):
    __name__ = 'yaxis'
    axis_name = 'y'  #: Read-only name identifying the axis.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # x in display coords, y in axes coords (to be updated at draw time by
        # _update_label_positions and _update_offset_text_position).
        self.label.set(
            x=0, y=0.5,
            verticalalignment='bottom', horizontalalignment='center',
            rotation='vertical', rotation_mode='anchor',
            transform=mtransforms.blended_transform_factory(
                mtransforms.IdentityTransform(), self.axes.transAxes),
        )
        self.label_position = 'left'
        # x in axes coords, y in display coords(!).
        self.offsetText.set(
            x=0, y=0.5,
            verticalalignment='baseline', horizontalalignment='left',
            transform=mtransforms.blended_transform_factory(
                self.axes.transAxes, mtransforms.IdentityTransform()),
            fontsize=mpl.rcParams['ytick.labelsize'],
            color=mpl.rcParams['ytick.color'],
        )
        self.offset_text_position = 'left'

    def contains(self, mouseevent):
        # docstring inherited
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info

        x, y = mouseevent.x, mouseevent.y
        try:
            trans = self.axes.transAxes.inverted()
            xaxes, yaxes = trans.transform((x, y))
        except ValueError:
            return False, {}
        (l, b), (r, t) = self.axes.transAxes.transform([(0, 0), (1, 1)])
        inaxis = 0 <= yaxes <= 1 and (
            l - self.pickradius < x < l or
            r < x < r + self.pickradius)
        return inaxis, {}

    def _get_tick(self, major):
        if major:
            tick_kw = self._major_tick_kw
        else:
            tick_kw = self._minor_tick_kw
        return YTick(self.axes, 0, major=major, **tick_kw)

    def set_label_position(self, position):
        """
        Set the label position (left or right)

        Parameters
        ----------
        position : {'left', 'right'}
        """
        self.label.set_rotation_mode('anchor')
        self.label.set_verticalalignment(_api.check_getitem({
            'left': 'bottom', 'right': 'top',
        }, position=position))
        self.label_position = position
        self.stale = True

    def _update_label_position(self, renderer):
        """
        Update the label position based on the bounding box enclosing
        all the ticklabels and axis spine
        """
        if not self._autolabelpos:
            return

        # get bounding boxes for this axis and any siblings
        # that have been set by `fig.align_ylabels()`
        bboxes, bboxes2 = self._get_tick_boxes_siblings(renderer=renderer)

        x, y = self.label.get_position()
        if self.label_position == 'left':
            try:
                spine = self.axes.spines['left']
                spinebbox = spine.get_transform().transform_path(
                    spine.get_path()).get_extents()
            except KeyError:
                # use axes if spine doesn't exist
                spinebbox = self.axes.bbox
            bbox = mtransforms.Bbox.union(bboxes + [spinebbox])
            left = bbox.x0
            self.label.set_position(
                (left - self.labelpad * self.figure.dpi / 72, y)
            )

        else:
            try:
                spine = self.axes.spines['right']
                spinebbox = spine.get_transform().transform_path(
                    spine.get_path()).get_extents()
            except KeyError:
                # use axes if spine doesn't exist
                spinebbox = self.axes.bbox
            bbox = mtransforms.Bbox.union(bboxes2 + [spinebbox])
            right = bbox.x1

            self.label.set_position(
                (right + self.labelpad * self.figure.dpi / 72, y)
            )

    def _update_offset_text_position(self, bboxes, bboxes2):
        """
        Update the offset_text position based on the sequence of bounding
        boxes of all the ticklabels
        """
        x, y = self.offsetText.get_position()
        top = self.axes.bbox.ymax
        self.offsetText.set_position(
            (x, top + self.OFFSETTEXTPAD * self.figure.dpi / 72)
        )

    def set_offset_position(self, position):
        """
        Parameters
        ----------
        position : {'left', 'right'}
        """
        x, y = self.offsetText.get_position()
        x = _api.check_getitem({'left': 0, 'right': 1}, position=position)

        self.offsetText.set_ha(position)
        self.offsetText.set_position((x, y))
        self.stale = True

    def get_text_widths(self, renderer):
        bbox, bbox2 = self.get_ticklabel_extents(renderer)
        # MGDTODO: Need a better way to get the pad
        padPixels = self.majorTicks[0].get_pad_pixels()

        left = 0.0
        if bbox.width:
            left += bbox.width + padPixels
        right = 0.0
        if bbox2.width:
            right += bbox2.width + padPixels

        if self.get_label_position() == 'left':
            left += self.label.get_window_extent(renderer).width + padPixels
        else:
            right += self.label.get_window_extent(renderer).width + padPixels
        return left, right

    def set_ticks_position(self, position):
        """
        Set the ticks position.

        Parameters
        ----------
        position : {'left', 'right', 'both', 'default', 'none'}
            'both' sets the ticks to appear on both positions, but does not
            change the tick labels.  'default' resets the tick positions to
            the default: ticks on both positions, labels at left.  'none'
            can be used if you don't want any ticks. 'none' and 'both'
            affect only the ticks, not the labels.
        """
        _api.check_in_list(['left', 'right', 'both', 'default', 'none'],
                           position=position)
        if position == 'right':
            self.set_tick_params(which='both', right=True, labelright=True,
                                 left=False, labelleft=False)
            self.set_offset_position(position)
        elif position == 'left':
            self.set_tick_params(which='both', right=False, labelright=False,
                                 left=True, labelleft=True)
            self.set_offset_position(position)
        elif position == 'both':
            self.set_tick_params(which='both', right=True,
                                 left=True)
        elif position == 'none':
            self.set_tick_params(which='both', right=False,
                                 left=False)
        elif position == 'default':
            self.set_tick_params(which='both', right=True, labelright=False,
                                 left=True, labelleft=True)
        else:
            assert False, "unhandled parameter not caught by _check_in_list"
        self.stale = True

    def tick_right(self):
        """
        Move ticks and ticklabels (if present) to the right of the axes.
        """
        label = True
        if 'label1On' in self._major_tick_kw:
            label = (self._major_tick_kw['label1On']
                     or self._major_tick_kw['label2On'])
        self.set_ticks_position('right')
        # if labels were turned off before this was called
        # leave them off
        self.set_tick_params(which='both', labelright=label)

    def tick_left(self):
        """
        Move ticks and ticklabels (if present) to the left of the axes.
        """
        label = True
        if 'label1On' in self._major_tick_kw:
            label = (self._major_tick_kw['label1On']
                     or self._major_tick_kw['label2On'])
        self.set_ticks_position('left')
        # if labels were turned off before this was called
        # leave them off
        self.set_tick_params(which='both', labelleft=label)

    def get_ticks_position(self):
        """
        Return the ticks position ("left", "right", "default", or "unknown").
        """
        return {1: "left", 2: "right",
                "default": "default", "unknown": "unknown"}[
                    self._get_ticks_position()]

    get_view_interval, set_view_interval = _make_getset_interval(
        "view", "viewLim", "intervaly")
    get_data_interval, set_data_interval = _make_getset_interval(
        "data", "dataLim", "intervaly")

    def get_minpos(self):
        return self.axes.dataLim.minposy

    def set_inverted(self, inverted):
        # docstring inherited
        a, b = self.get_view_interval()
        # cast to bool to avoid bad interaction between python 3.8 and np.bool_
        self.axes.set_ylim(sorted((a, b), reverse=bool(inverted)), auto=None)

    def set_default_intervals(self):
        # docstring inherited
        ymin, ymax = 0., 1.
        dataMutated = self.axes.dataLim.mutatedy()
        viewMutated = self.axes.viewLim.mutatedy()
        if not dataMutated or not viewMutated:
            if self.converter is not None:
                info = self.converter.axisinfo(self.units, self)
                if info.default_limits is not None:
                    valmin, valmax = info.default_limits
                    ymin = self.converter.convert(valmin, self.units, self)
                    ymax = self.converter.convert(valmax, self.units, self)
            if not dataMutated:
                self.axes.dataLim.intervaly = ymin, ymax
            if not viewMutated:
                self.axes.viewLim.intervaly = ymin, ymax
        self.stale = True

    def get_tick_space(self):
        ends = mtransforms.Bbox.from_bounds(0, 0, 1, 1)
        ends = ends.transformed(self.axes.transAxes -
                                self.figure.dpi_scale_trans)
        length = ends.height * 72
        # Having a spacing of at least 2 just looks good.
        size = self._get_tick_label_size('y') * 2
        if size > 0:
            return int(np.floor(length / size))
        else:
            return 2**31 - 1
