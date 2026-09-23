@_docstring.interpd
@_api.define_aliases({
    "color": ["c"],
    "fontfamily": ["family"],
    "fontproperties": ["font", "font_properties"],
    "horizontalalignment": ["ha"],
    "multialignment": ["ma"],
    "fontname": ["name"],
    "fontsize": ["size"],
    "fontstretch": ["stretch"],
    "fontstyle": ["style"],
    "fontvariant": ["variant"],
    "verticalalignment": ["va"],
    "fontweight": ["weight"],
})
class Text(Artist):
    """Handle storing and drawing of text in window or data coordinates."""

    zorder = 3

    def __repr__(self):
        return "Text(%s, %s, %s)" % (self._x, self._y, repr(self._text))

    @_api.make_keyword_only("3.6", name="color")
    def __init__(self,
                 x=0, y=0, text='',
                 color=None,           # defaults to rc params
                 verticalalignment='baseline',
                 horizontalalignment='left',
                 multialignment=None,
                 fontproperties=None,  # defaults to FontProperties()
                 rotation=None,
                 linespacing=None,
                 rotation_mode=None,
                 usetex=None,          # defaults to rcParams['text.usetex']
                 wrap=False,
                 transform_rotates_text=False,
                 *,
                 parse_math=None,    # defaults to rcParams['text.parse_math']
                 **kwargs
                 ):
        """
        Create a `.Text` instance at *x*, *y* with string *text*.

        The text is aligned relative to the anchor point (*x*, *y*) according
        to ``horizontalalignment`` (default: 'left') and ``verticalalignment``
        (default: 'bottom'). See also
        :doc:`/gallery/text_labels_and_annotations/text_alignment`.

        While Text accepts the 'label' keyword argument, by default it is not
        added to the handles of a legend.

        Valid keyword arguments are:

        %(Text:kwdoc)s
        """
        super().__init__()
        self._x, self._y = x, y
        self._text = ''
        self.set_text(text)
        self.set_color(
            color if color is not None else mpl.rcParams["text.color"])
        self.set_fontproperties(fontproperties)
        self.set_usetex(usetex)
        self.set_parse_math(parse_math if parse_math is not None else
                            mpl.rcParams['text.parse_math'])
        self.set_wrap(wrap)
        self.set_verticalalignment(verticalalignment)
        self.set_horizontalalignment(horizontalalignment)
        self._multialignment = multialignment
        self.set_rotation(rotation)
        self._transform_rotates_text = transform_rotates_text
        self._bbox_patch = None  # a FancyBboxPatch instance
        self._renderer = None
        if linespacing is None:
            linespacing = 1.2  # Maybe use rcParam later.
        self.set_linespacing(linespacing)
        self.set_rotation_mode(rotation_mode)
        self.update(kwargs)

    def update(self, kwargs):
        # docstring inherited
        kwargs = cbook.normalize_kwargs(kwargs, Text)
        sentinel = object()  # bbox can be None, so use another sentinel.
        # Update fontproperties first, as it has lowest priority.
        fontproperties = kwargs.pop("fontproperties", sentinel)
        if fontproperties is not sentinel:
            self.set_fontproperties(fontproperties)
        # Update bbox last, as it depends on font properties.
        bbox = kwargs.pop("bbox", sentinel)
        super().update(kwargs)
        if bbox is not sentinel:
            self.set_bbox(bbox)

    def __getstate__(self):
        d = super().__getstate__()
        # remove the cached _renderer (if it exists)
        d['_renderer'] = None
        return d

    def contains(self, mouseevent):
        """
        Return whether the mouse event occurred inside the axis-aligned
        bounding-box of the text.
        """
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info

        if not self.get_visible() or self._renderer is None:
            return False, {}

        # Explicitly use Text.get_window_extent(self) and not
        # self.get_window_extent() so that Annotation.contains does not
        # accidentally cover the entire annotation bounding box.
        bbox = Text.get_window_extent(self)
        inside = (bbox.x0 <= mouseevent.x <= bbox.x1
                  and bbox.y0 <= mouseevent.y <= bbox.y1)

        cattr = {}
        # if the text has a surrounding patch, also check containment for it,
        # and merge the results with the results for the text.
        if self._bbox_patch:
            patch_inside, patch_cattr = self._bbox_patch.contains(mouseevent)
            inside = inside or patch_inside
            cattr["bbox_patch"] = patch_cattr

        return inside, cattr

    def _get_xy_display(self):
        """
        Get the (possibly unit converted) transformed x, y in display coords.
        """
        x, y = self.get_unitless_position()
        return self.get_transform().transform((x, y))

    def _get_multialignment(self):
        if self._multialignment is not None:
            return self._multialignment
        else:
            return self._horizontalalignment

    def get_rotation(self):
        """Return the text angle in degrees between 0 and 360."""
        if self.get_transform_rotates_text():
            return self.get_transform().transform_angles(
                [self._rotation], [self.get_unitless_position()]).item(0)
        else:
            return self._rotation

    def get_transform_rotates_text(self):
        """
        Return whether rotations of the transform affect the text direction.
        """
        return self._transform_rotates_text

    def set_rotation_mode(self, m):
        """
        Set text rotation mode.

        Parameters
        ----------
        m : {None, 'default', 'anchor'}
            If ``None`` or ``"default"``, the text will be first rotated, then
            aligned according to their horizontal and vertical alignments.  If
            ``"anchor"``, then alignment occurs before rotation.
        """
        _api.check_in_list(["anchor", "default", None], rotation_mode=m)
        self._rotation_mode = m
        self.stale = True

    def get_rotation_mode(self):
        """Return the text rotation mode."""
        return self._rotation_mode

    def update_from(self, other):
        # docstring inherited
        super().update_from(other)
        self._color = other._color
        self._multialignment = other._multialignment
        self._verticalalignment = other._verticalalignment
        self._horizontalalignment = other._horizontalalignment
        self._fontproperties = other._fontproperties.copy()
        self._usetex = other._usetex
        self._rotation = other._rotation
        self._transform_rotates_text = other._transform_rotates_text
        self._picker = other._picker
        self._linespacing = other._linespacing
        self.stale = True

    def _get_layout(self, renderer):
        """
        Return the extent (bbox) of the text together with
        multiple-alignment information. Note that it returns an extent
        of a rotated text when necessary.
        """
        thisx, thisy = 0.0, 0.0
        text = self.get_text()
        lines = [text] if self.get_usetex() else text.split("\n")  # Not empty.

        ws = []
        hs = []
        xs = []
        ys = []

        # Full vertical extent of font, including ascenders and descenders:
        _, lp_h, lp_d = _get_text_metrics_with_cache(
            renderer, "lp", self._fontproperties,
            ismath="TeX" if self.get_usetex() else False, dpi=self.figure.dpi)
        min_dy = (lp_h - lp_d) * self._linespacing

        for i, line in enumerate(lines):
            clean_line, ismath = self._preprocess_math(line)
            if clean_line:
                w, h, d = _get_text_metrics_with_cache(
                    renderer, clean_line, self._fontproperties,
                    ismath=ismath, dpi=self.figure.dpi)
            else:
                w = h = d = 0

            # For multiline text, increase the line spacing when the text
            # net-height (excluding baseline) is larger than that of a "l"
            # (e.g., use of superscripts), which seems what TeX does.
            h = max(h, lp_h)
            d = max(d, lp_d)

            ws.append(w)
            hs.append(h)

            # Metrics of the last line that are needed later:
            baseline = (h - d) - thisy

            if i == 0:
                # position at baseline
                thisy = -(h - d)
            else:
                # put baseline a good distance from bottom of previous line
                thisy -= max(min_dy, (h - d) * self._linespacing)

            xs.append(thisx)  # == 0.
            ys.append(thisy)

            thisy -= d

        # Metrics of the last line that are needed later:
        descent = d

        # Bounding box definition:
        width = max(ws)
        xmin = 0
        xmax = width
        ymax = 0
        ymin = ys[-1] - descent  # baseline of last line minus its descent

        # get the rotation matrix
        M = Affine2D().rotate_deg(self.get_rotation())

        # now offset the individual text lines within the box
        malign = self._get_multialignment()
        if malign == 'left':
            offset_layout = [(x, y) for x, y in zip(xs, ys)]
        elif malign == 'center':
            offset_layout = [(x + width / 2 - w / 2, y)
                             for x, y, w in zip(xs, ys, ws)]
        elif malign == 'right':
            offset_layout = [(x + width - w, y)
                             for x, y, w in zip(xs, ys, ws)]

        # the corners of the unrotated bounding box
        corners_horiz = np.array(
            [(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)])

        # now rotate the bbox
        corners_rotated = M.transform(corners_horiz)
        # compute the bounds of the rotated box
        xmin = corners_rotated[:, 0].min()
        xmax = corners_rotated[:, 0].max()
        ymin = corners_rotated[:, 1].min()
        ymax = corners_rotated[:, 1].max()
        width = xmax - xmin
        height = ymax - ymin

        # Now move the box to the target position offset the display
        # bbox by alignment
        halign = self._horizontalalignment
        valign = self._verticalalignment

        rotation_mode = self.get_rotation_mode()
        if rotation_mode != "anchor":
            # compute the text location in display coords and the offsets
            # necessary to align the bbox with that location
            if halign == 'center':
                offsetx = (xmin + xmax) / 2
            elif halign == 'right':
                offsetx = xmax
            else:
                offsetx = xmin

            if valign == 'center':
                offsety = (ymin + ymax) / 2
            elif valign == 'top':
                offsety = ymax
            elif valign == 'baseline':
                offsety = ymin + descent
            elif valign == 'center_baseline':
                offsety = ymin + height - baseline / 2.0
            else:
                offsety = ymin
        else:
            xmin1, ymin1 = corners_horiz[0]
            xmax1, ymax1 = corners_horiz[2]

            if halign == 'center':
                offsetx = (xmin1 + xmax1) / 2.0
            elif halign == 'right':
                offsetx = xmax1
            else:
                offsetx = xmin1

            if valign == 'center':
                offsety = (ymin1 + ymax1) / 2.0
            elif valign == 'top':
                offsety = ymax1
            elif valign == 'baseline':
                offsety = ymax1 - baseline
            elif valign == 'center_baseline':
                offsety = ymax1 - baseline / 2.0
            else:
                offsety = ymin1

            offsetx, offsety = M.transform((offsetx, offsety))

        xmin -= offsetx
        ymin -= offsety

        bbox = Bbox.from_bounds(xmin, ymin, width, height)

        # now rotate the positions around the first (x, y) position
        xys = M.transform(offset_layout) - (offsetx, offsety)

        return bbox, list(zip(lines, zip(ws, hs), *xys.T)), descent

    def set_bbox(self, rectprops):
        """
        Draw a bounding box around self.

        Parameters
        ----------
        rectprops : dict with properties for `.patches.FancyBboxPatch`
             The default boxstyle is 'square'. The mutation
             scale of the `.patches.FancyBboxPatch` is set to the fontsize.

        Examples
        --------
        ::

            t.set_bbox(dict(facecolor='red', alpha=0.5))
        """

        if rectprops is not None:
            props = rectprops.copy()
            boxstyle = props.pop("boxstyle", None)
            pad = props.pop("pad", None)
            if boxstyle is None:
                boxstyle = "square"
                if pad is None:
                    pad = 4  # points
                pad /= self.get_size()  # to fraction of font size
            else:
                if pad is None:
                    pad = 0.3
            # boxstyle could be a callable or a string
            if isinstance(boxstyle, str) and "pad" not in boxstyle:
                boxstyle += ",pad=%0.2f" % pad
            self._bbox_patch = FancyBboxPatch(
                (0, 0), 1, 1,
                boxstyle=boxstyle, transform=IdentityTransform(), **props)
        else:
            self._bbox_patch = None

        self._update_clip_properties()

    def get_bbox_patch(self):
        """
        Return the bbox Patch, or None if the `.patches.FancyBboxPatch`
        is not made.
        """
        return self._bbox_patch

    def update_bbox_position_size(self, renderer):
        """
        Update the location and the size of the bbox.

        This method should be used when the position and size of the bbox needs
        to be updated before actually drawing the bbox.
        """
        if self._bbox_patch:
            # don't use self.get_unitless_position here, which refers to text
            # position in Text:
            posx = float(self.convert_xunits(self._x))
            posy = float(self.convert_yunits(self._y))
            posx, posy = self.get_transform().transform((posx, posy))

            x_box, y_box, w_box, h_box = _get_textbox(self, renderer)
            self._bbox_patch.set_bounds(0., 0., w_box, h_box)
            self._bbox_patch.set_transform(
                Affine2D()
                .rotate_deg(self.get_rotation())
                .translate(posx + x_box, posy + y_box))
            fontsize_in_pixel = renderer.points_to_pixels(self.get_size())
            self._bbox_patch.set_mutation_scale(fontsize_in_pixel)

    def _update_clip_properties(self):
        clipprops = dict(clip_box=self.clipbox,
                         clip_path=self._clippath,
                         clip_on=self._clipon)
        if self._bbox_patch:
            self._bbox_patch.update(clipprops)

    def set_clip_box(self, clipbox):
        # docstring inherited.
        super().set_clip_box(clipbox)
        self._update_clip_properties()

    def set_clip_path(self, path, transform=None):
        # docstring inherited.
        super().set_clip_path(path, transform)
        self._update_clip_properties()

    def set_clip_on(self, b):
        # docstring inherited.
        super().set_clip_on(b)
        self._update_clip_properties()

    def get_wrap(self):
        """Return whether the text can be wrapped."""
        return self._wrap

    def set_wrap(self, wrap):
        """
        Set whether the text can be wrapped.

        Parameters
        ----------
        wrap : bool

        Notes
        -----
        Wrapping does not work together with
        ``savefig(..., bbox_inches='tight')`` (which is also used internally
        by ``%matplotlib inline`` in IPython/Jupyter). The 'tight' setting
        rescales the canvas to accommodate all content and happens before
        wrapping.
        """
        self._wrap = wrap

    def _get_wrap_line_width(self):
        """
        Return the maximum line width for wrapping text based on the current
        orientation.
        """
        x0, y0 = self.get_transform().transform(self.get_position())
        figure_box = self.get_figure().get_window_extent()

        # Calculate available width based on text alignment
        alignment = self.get_horizontalalignment()
        self.set_rotation_mode('anchor')
        rotation = self.get_rotation()

        left = self._get_dist_to_box(rotation, x0, y0, figure_box)
        right = self._get_dist_to_box(
            (180 + rotation) % 360, x0, y0, figure_box)

        if alignment == 'left':
            line_width = left
        elif alignment == 'right':
            line_width = right
        else:
            line_width = 2 * min(left, right)

        return line_width

    def _get_dist_to_box(self, rotation, x0, y0, figure_box):
        """
        Return the distance from the given points to the boundaries of a
        rotated box, in pixels.
        """
        if rotation > 270:
            quad = rotation - 270
            h1 = y0 / math.cos(math.radians(quad))
            h2 = (figure_box.x1 - x0) / math.cos(math.radians(90 - quad))
        elif rotation > 180:
            quad = rotation - 180
            h1 = x0 / math.cos(math.radians(quad))
            h2 = y0 / math.cos(math.radians(90 - quad))
        elif rotation > 90:
            quad = rotation - 90
            h1 = (figure_box.y1 - y0) / math.cos(math.radians(quad))
            h2 = x0 / math.cos(math.radians(90 - quad))
        else:
            h1 = (figure_box.x1 - x0) / math.cos(math.radians(rotation))
            h2 = (figure_box.y1 - y0) / math.cos(math.radians(90 - rotation))

        return min(h1, h2)

    def _get_rendered_text_width(self, text):
        """
        Return the width of a given text string, in pixels.
        """
        w, h, d = self._renderer.get_text_width_height_descent(
            text,
            self.get_fontproperties(),
            False)
        return math.ceil(w)

    def _get_wrapped_text(self):
        """
        Return a copy of the text string with new lines added so that the text
        is wrapped relative to the parent figure (if `get_wrap` is True).
        """
        if not self.get_wrap():
            return self.get_text()

        # Not fit to handle breaking up latex syntax correctly, so
        # ignore latex for now.
        if self.get_usetex():
            return self.get_text()

        # Build the line incrementally, for a more accurate measure of length
        line_width = self._get_wrap_line_width()
        wrapped_lines = []

        # New lines in the user's text force a split
        unwrapped_lines = self.get_text().split('\n')

        # Now wrap each individual unwrapped line
        for unwrapped_line in unwrapped_lines:

            sub_words = unwrapped_line.split(' ')
            # Remove items from sub_words as we go, so stop when empty
            while len(sub_words) > 0:
                if len(sub_words) == 1:
                    # Only one word, so just add it to the end
                    wrapped_lines.append(sub_words.pop(0))
                    continue

                for i in range(2, len(sub_words) + 1):
                    # Get width of all words up to and including here
                    line = ' '.join(sub_words[:i])
                    current_width = self._get_rendered_text_width(line)

                    # If all these words are too wide, append all not including
                    # last word
                    if current_width > line_width:
                        wrapped_lines.append(' '.join(sub_words[:i - 1]))
                        sub_words = sub_words[i - 1:]
                        break

                    # Otherwise if all words fit in the width, append them all
                    elif i == len(sub_words):
                        wrapped_lines.append(' '.join(sub_words[:i]))
                        sub_words = []
                        break

        return '\n'.join(wrapped_lines)

    @artist.allow_rasterization
    def draw(self, renderer):
        # docstring inherited

        if renderer is not None:
            self._renderer = renderer
        if not self.get_visible():
            return
        if self.get_text() == '':
            return

        renderer.open_group('text', self.get_gid())

        with self._cm_set(text=self._get_wrapped_text()):
            bbox, info, descent = self._get_layout(renderer)
            trans = self.get_transform()

            # don't use self.get_position here, which refers to text
            # position in Text:
            posx = float(self.convert_xunits(self._x))
            posy = float(self.convert_yunits(self._y))
            posx, posy = trans.transform((posx, posy))
            if not np.isfinite(posx) or not np.isfinite(posy):
                _log.warning("posx and posy should be finite values")
                return
            canvasw, canvash = renderer.get_canvas_width_height()

            # Update the location and size of the bbox
            # (`.patches.FancyBboxPatch`), and draw it.
            if self._bbox_patch:
                self.update_bbox_position_size(renderer)
                self._bbox_patch.draw(renderer)

            gc = renderer.new_gc()
            gc.set_foreground(self.get_color())
            gc.set_alpha(self.get_alpha())
            gc.set_url(self._url)
            self._set_gc_clip(gc)

            angle = self.get_rotation()

            for line, wh, x, y in info:

                mtext = self if len(info) == 1 else None
                x = x + posx
                y = y + posy
                if renderer.flipy():
                    y = canvash - y
                clean_line, ismath = self._preprocess_math(line)

                if self.get_path_effects():
                    from matplotlib.patheffects import PathEffectRenderer
                    textrenderer = PathEffectRenderer(
                        self.get_path_effects(), renderer)
                else:
                    textrenderer = renderer

                if self.get_usetex():
                    textrenderer.draw_tex(gc, x, y, clean_line,
                                          self._fontproperties, angle,
                                          mtext=mtext)
                else:
                    textrenderer.draw_text(gc, x, y, clean_line,
                                           self._fontproperties, angle,
                                           ismath=ismath, mtext=mtext)

        gc.restore()
        renderer.close_group('text')
        self.stale = False

    def get_color(self):
        """Return the color of the text."""
        return self._color

    def get_fontproperties(self):
        """Return the `.font_manager.FontProperties`."""
        return self._fontproperties

    def get_fontfamily(self):
        """
        Return the list of font families used for font lookup.

        See Also
        --------
        .font_manager.FontProperties.get_family
        """
        return self._fontproperties.get_family()

    def get_fontname(self):
        """
        Return the font name as a string.

        See Also
        --------
        .font_manager.FontProperties.get_name
        """
        return self._fontproperties.get_name()

    def get_fontstyle(self):
        """
        Return the font style as a string.

        See Also
        --------
        .font_manager.FontProperties.get_style
        """
        return self._fontproperties.get_style()

    def get_fontsize(self):
        """
        Return the font size as an integer.

        See Also
        --------
        .font_manager.FontProperties.get_size_in_points
        """
        return self._fontproperties.get_size_in_points()

    def get_fontvariant(self):
        """
        Return the font variant as a string.

        See Also
        --------
        .font_manager.FontProperties.get_variant
        """
        return self._fontproperties.get_variant()

    def get_fontweight(self):
        """
        Return the font weight as a string or a number.

        See Also
        --------
        .font_manager.FontProperties.get_weight
        """
        return self._fontproperties.get_weight()

    def get_stretch(self):
        """
        Return the font stretch as a string or a number.

        See Also
        --------
        .font_manager.FontProperties.get_stretch
        """
        return self._fontproperties.get_stretch()

    def get_horizontalalignment(self):
        """
        Return the horizontal alignment as a string.  Will be one of
        'left', 'center' or 'right'.
        """
        return self._horizontalalignment

    def get_unitless_position(self):
        """Return the (x, y) unitless position of the text."""
        # This will get the position with all unit information stripped away.
        # This is here for convenience since it is done in several locations.
        x = float(self.convert_xunits(self._x))
        y = float(self.convert_yunits(self._y))
        return x, y

    def get_position(self):
        """Return the (x, y) position of the text."""
        # This should return the same data (possible unitized) as was
        # specified with 'set_x' and 'set_y'.
        return self._x, self._y

    # When removing, also remove the hash(color) check in set_color()
    @_api.deprecated("3.5")
    def get_prop_tup(self, renderer=None):
        """
        Return a hashable tuple of properties.

        Not intended to be human readable, but useful for backends who
        want to cache derived information about text (e.g., layouts) and
        need to know if the text has changed.
        """
        x, y = self.get_unitless_position()
        renderer = renderer or self._renderer
        return (x, y, self.get_text(), self._color,
                self._verticalalignment, self._horizontalalignment,
                hash(self._fontproperties),
                self._rotation, self._rotation_mode,
                self._transform_rotates_text,
                self.figure.dpi, weakref.ref(renderer),
                self._linespacing
                )

    def get_text(self):
        """Return the text string."""
        return self._text

    def get_verticalalignment(self):
        """
        Return the vertical alignment as a string.  Will be one of
        'top', 'center', 'bottom', 'baseline' or 'center_baseline'.
        """
        return self._verticalalignment

    def get_window_extent(self, renderer=None, dpi=None):
        """
        Return the `.Bbox` bounding the text, in display units.

        In addition to being used internally, this is useful for specifying
        clickable regions in a png file on a web page.

        Parameters
        ----------
        renderer : Renderer, optional
            A renderer is needed to compute the bounding box.  If the artist
            has already been drawn, the renderer is cached; thus, it is only
            necessary to pass this argument when calling `get_window_extent`
            before the first draw.  In practice, it is usually easier to
            trigger a draw first, e.g. by calling
            `~.Figure.draw_without_rendering` or ``plt.show()``.

        dpi : float, optional
            The dpi value for computing the bbox, defaults to
            ``self.figure.dpi`` (*not* the renderer dpi); should be set e.g. if
            to match regions with a figure saved with a custom dpi value.
        """
        if not self.get_visible():
            return Bbox.unit()
        if dpi is None:
            dpi = self.figure.dpi
        if self.get_text() == '':
            with cbook._setattr_cm(self.figure, dpi=dpi):
                tx, ty = self._get_xy_display()
                return Bbox.from_bounds(tx, ty, 0, 0)

        if renderer is not None:
            self._renderer = renderer
        if self._renderer is None:
            self._renderer = self.figure._get_renderer()
        if self._renderer is None:
            raise RuntimeError(
                "Cannot get window extent of text w/o renderer. You likely "
                "want to call 'figure.draw_without_rendering()' first.")

        with cbook._setattr_cm(self.figure, dpi=dpi):
            bbox, info, descent = self._get_layout(self._renderer)
            x, y = self.get_unitless_position()
            x, y = self.get_transform().transform((x, y))
            bbox = bbox.translated(x, y)
            return bbox

    def set_backgroundcolor(self, color):
        """
        Set the background color of the text by updating the bbox.

        Parameters
        ----------
        color : color

        See Also
        --------
        .set_bbox : To change the position of the bounding box
        """
        if self._bbox_patch is None:
            self.set_bbox(dict(facecolor=color, edgecolor=color))
        else:
            self._bbox_patch.update(dict(facecolor=color))

        self._update_clip_properties()
        self.stale = True

    def set_color(self, color):
        """
        Set the foreground color of the text

        Parameters
        ----------
        color : color
        """
        # "auto" is only supported by axisartist, but we can just let it error
        # out at draw time for simplicity.
        if not cbook._str_equal(color, "auto"):
            mpl.colors._check_color_like(color=color)
        # Make sure it is hashable, or get_prop_tup will fail (remove this once
        # get_prop_tup is removed).
        try:
            hash(color)
        except TypeError:
            color = tuple(color)
        self._color = color
        self.stale = True

    def set_horizontalalignment(self, align):
        """
        Set the horizontal alignment relative to the anchor point.

        See also :doc:`/gallery/text_labels_and_annotations/text_alignment`.

        Parameters
        ----------
        align : {'left', 'center', 'right'}
        """
        _api.check_in_list(['center', 'right', 'left'], align=align)
        self._horizontalalignment = align
        self.stale = True

    def set_multialignment(self, align):
        """
        Set the text alignment for multiline texts.

        The layout of the bounding box of all the lines is determined by the
        horizontalalignment and verticalalignment properties. This property
        controls the alignment of the text lines within that box.

        Parameters
        ----------
        align : {'left', 'right', 'center'}
        """
        _api.check_in_list(['center', 'right', 'left'], align=align)
        self._multialignment = align
        self.stale = True

    def set_linespacing(self, spacing):
        """
        Set the line spacing as a multiple of the font size.

        The default line spacing is 1.2.

        Parameters
        ----------
        spacing : float (multiple of font size)
        """
        _api.check_isinstance(Real, spacing=spacing)
        self._linespacing = spacing
        self.stale = True

    def set_fontfamily(self, fontname):
        """
        Set the font family.  May be either a single string, or a list of
        strings in decreasing priority.  Each string may be either a real font
        name or a generic font class name.  If the latter, the specific font
        names will be looked up in the corresponding rcParams.

        If a `Text` instance is constructed with ``fontfamily=None``, then the
        font is set to :rc:`font.family`, and the
        same is done when `set_fontfamily()` is called on an existing
        `Text` instance.

        Parameters
        ----------
        fontname : {FONTNAME, 'serif', 'sans-serif', 'cursive', 'fantasy', \
'monospace'}

        See Also
        --------
        .font_manager.FontProperties.set_family
        """
        self._fontproperties.set_family(fontname)
        self.stale = True

    def set_fontvariant(self, variant):
        """
        Set the font variant.

        Parameters
        ----------
        variant : {'normal', 'small-caps'}

        See Also
        --------
        .font_manager.FontProperties.set_variant
        """
        self._fontproperties.set_variant(variant)
        self.stale = True

    def set_fontstyle(self, fontstyle):
        """
        Set the font style.

        Parameters
        ----------
        fontstyle : {'normal', 'italic', 'oblique'}

        See Also
        --------
        .font_manager.FontProperties.set_style
        """
        self._fontproperties.set_style(fontstyle)
        self.stale = True

    def set_fontsize(self, fontsize):
        """
        Set the font size.

        Parameters
        ----------
        fontsize : float or {'xx-small', 'x-small', 'small', 'medium', \
'large', 'x-large', 'xx-large'}
            If float, the fontsize in points. The string values denote sizes
            relative to the default font size.

        See Also
        --------
        .font_manager.FontProperties.set_size
        """
        self._fontproperties.set_size(fontsize)
        self.stale = True

    def get_math_fontfamily(self):
        """
        Return the font family name for math text rendered by Matplotlib.

        The default value is :rc:`mathtext.fontset`.

        See Also
        --------
        set_math_fontfamily
        """
        return self._fontproperties.get_math_fontfamily()

    def set_math_fontfamily(self, fontfamily):
        """
        Set the font family for math text rendered by Matplotlib.

        This does only affect Matplotlib's own math renderer. It has no effect
        when rendering with TeX (``usetex=True``).

        Parameters
        ----------
        fontfamily : str
            The name of the font family.

            Available font families are defined in the
            :ref:`matplotlibrc.template file
            <customizing-with-matplotlibrc-files>`.

        See Also
        --------
        get_math_fontfamily
        """
        self._fontproperties.set_math_fontfamily(fontfamily)

    def set_fontweight(self, weight):
        """
        Set the font weight.

        Parameters
        ----------
        weight : {a numeric value in range 0-1000, 'ultralight', 'light', \
'normal', 'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', \
'demi', 'bold', 'heavy', 'extra bold', 'black'}

        See Also
        --------
        .font_manager.FontProperties.set_weight
        """
        self._fontproperties.set_weight(weight)
        self.stale = True

    def set_fontstretch(self, stretch):
        """
        Set the font stretch (horizontal condensation or expansion).

        Parameters
        ----------
        stretch : {a numeric value in range 0-1000, 'ultra-condensed', \
'extra-condensed', 'condensed', 'semi-condensed', 'normal', 'semi-expanded', \
'expanded', 'extra-expanded', 'ultra-expanded'}

        See Also
        --------
        .font_manager.FontProperties.set_stretch
        """
        self._fontproperties.set_stretch(stretch)
        self.stale = True

    def set_position(self, xy):
        """
        Set the (*x*, *y*) position of the text.

        Parameters
        ----------
        xy : (float, float)
        """
        self.set_x(xy[0])
        self.set_y(xy[1])

    def set_x(self, x):
        """
        Set the *x* position of the text.

        Parameters
        ----------
        x : float
        """
        self._x = x
        self.stale = True

    def set_y(self, y):
        """
        Set the *y* position of the text.

        Parameters
        ----------
        y : float
        """
        self._y = y
        self.stale = True

    def set_rotation(self, s):
        """
        Set the rotation of the text.

        Parameters
        ----------
        s : float or {'vertical', 'horizontal'}
            The rotation angle in degrees in mathematically positive direction
            (counterclockwise). 'horizontal' equals 0, 'vertical' equals 90.
        """
        if isinstance(s, Real):
            self._rotation = float(s) % 360
        elif cbook._str_equal(s, 'horizontal') or s is None:
            self._rotation = 0.
        elif cbook._str_equal(s, 'vertical'):
            self._rotation = 90.
        else:
            raise ValueError("rotation must be 'vertical', 'horizontal' or "
                             f"a number, not {s}")
        self.stale = True

    def set_transform_rotates_text(self, t):
        """
        Whether rotations of the transform affect the text direction.

        Parameters
        ----------
        t : bool
        """
        self._transform_rotates_text = t
        self.stale = True

    def set_verticalalignment(self, align):
        """
        Set the vertical alignment relative to the anchor point.

        See also :doc:`/gallery/text_labels_and_annotations/text_alignment`.

        Parameters
        ----------
        align : {'bottom', 'baseline', 'center', 'center_baseline', 'top'}
        """
        _api.check_in_list(
            ['top', 'bottom', 'center', 'baseline', 'center_baseline'],
            align=align)
        self._verticalalignment = align
        self.stale = True

    def set_text(self, s):
        r"""
        Set the text string *s*.

        It may contain newlines (``\n``) or math in LaTeX syntax.

        Parameters
        ----------
        s : object
            Any object gets converted to its `str` representation, except for
            ``None`` which is converted to an empty string.
        """
        if s is None:
            s = ''
        if s != self._text:
            self._text = str(s)
            self.stale = True

    def _preprocess_math(self, s):
        """
        Return the string *s* after mathtext preprocessing, and the kind of
        mathtext support needed.

        - If *self* is configured to use TeX, return *s* unchanged except that
          a single space gets escaped, and the flag "TeX".
        - Otherwise, if *s* is mathtext (has an even number of unescaped dollar
          signs) and ``parse_math`` is not set to False, return *s* and the
          flag True.
        - Otherwise, return *s* with dollar signs unescaped, and the flag
          False.
        """
        if self.get_usetex():
            if s == " ":
                s = r"\ "
            return s, "TeX"
        elif not self.get_parse_math():
            return s, False
        elif cbook.is_math_text(s):
            return s, True
        else:
            return s.replace(r"\$", "$"), False

    def set_fontproperties(self, fp):
        """
        Set the font properties that control the text.

        Parameters
        ----------
        fp : `.font_manager.FontProperties` or `str` or `pathlib.Path`
            If a `str`, it is interpreted as a fontconfig pattern parsed by
            `.FontProperties`.  If a `pathlib.Path`, it is interpreted as the
            absolute path to a font file.
        """
        self._fontproperties = FontProperties._from_any(fp).copy()
        self.stale = True

    def set_usetex(self, usetex):
        """
        Parameters
        ----------
        usetex : bool or None
            Whether to render using TeX, ``None`` means to use
            :rc:`text.usetex`.
        """
        if usetex is None:
            self._usetex = mpl.rcParams['text.usetex']
        else:
            self._usetex = bool(usetex)
        self.stale = True

    def get_usetex(self):
        """Return whether this `Text` object uses TeX for rendering."""
        return self._usetex

    def set_parse_math(self, parse_math):
        """
        Override switch to disable any mathtext parsing for this `Text`.

        Parameters
        ----------
        parse_math : bool
            If False, this `Text` will never use mathtext.  If True, mathtext
            will be used if there is an even number of unescaped dollar signs.
        """
        self._parse_math = bool(parse_math)

    def get_parse_math(self):
        """Return whether mathtext parsing is considered for this `Text`."""
        return self._parse_math

    def set_fontname(self, fontname):
        """
        Alias for `set_family`.

        One-way alias only: the getter differs.

        Parameters
        ----------
        fontname : {FONTNAME, 'serif', 'sans-serif', 'cursive', 'fantasy', \
'monospace'}

        See Also
        --------
        .font_manager.FontProperties.set_family

        """
        return self.set_family(fontname)
