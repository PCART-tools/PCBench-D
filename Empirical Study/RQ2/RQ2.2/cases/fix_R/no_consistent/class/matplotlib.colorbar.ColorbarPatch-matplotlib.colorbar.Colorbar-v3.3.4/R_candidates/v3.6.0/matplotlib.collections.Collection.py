@_api.define_aliases({
    "antialiased": ["antialiaseds", "aa"],
    "edgecolor": ["edgecolors", "ec"],
    "facecolor": ["facecolors", "fc"],
    "linestyle": ["linestyles", "dashes", "ls"],
    "linewidth": ["linewidths", "lw"],
    "offset_transform": ["transOffset"],
})
class Collection(artist.Artist, cm.ScalarMappable):
    r"""
    Base class for Collections. Must be subclassed to be usable.

    A Collection represents a sequence of `.Patch`\es that can be drawn
    more efficiently together than individually. For example, when a single
    path is being drawn repeatedly at different offsets, the renderer can
    typically execute a ``draw_marker()`` call much more efficiently than a
    series of repeated calls to ``draw_path()`` with the offsets put in
    one-by-one.

    Most properties of a collection can be configured per-element. Therefore,
    Collections have "plural" versions of many of the properties of a `.Patch`
    (e.g. `.Collection.get_paths` instead of `.Patch.get_path`). Exceptions are
    the *zorder*, *hatch*, *pickradius*, *capstyle* and *joinstyle* properties,
    which can only be set globally for the whole collection.

    Besides these exceptions, all properties can be specified as single values
    (applying to all elements) or sequences of values. The property of the
    ``i``\th element of the collection is::

      prop[i % len(prop)]

    Each Collection can optionally be used as its own `.ScalarMappable` by
    passing the *norm* and *cmap* parameters to its constructor. If the
    Collection's `.ScalarMappable` matrix ``_A`` has been set (via a call
    to `.Collection.set_array`), then at draw time this internal scalar
    mappable will be used to set the ``facecolors`` and ``edgecolors``,
    ignoring those that were manually passed in.
    """
    #: Either a list of 3x3 arrays or an Nx3x3 array (representing N
    #: transforms), suitable for the `all_transforms` argument to
    #: `~matplotlib.backend_bases.RendererBase.draw_path_collection`;
    #: each 3x3 array is used to initialize an
    #: `~matplotlib.transforms.Affine2D` object.
    #: Each kind of collection defines this based on its arguments.
    _transforms = np.empty((0, 3, 3))

    # Whether to draw an edge by default.  Set on a
    # subclass-by-subclass basis.
    _edge_default = False

    @_docstring.interpd
    @_api.make_keyword_only("3.6", name="edgecolors")
    def __init__(self,
                 edgecolors=None,
                 facecolors=None,
                 linewidths=None,
                 linestyles='solid',
                 capstyle=None,
                 joinstyle=None,
                 antialiaseds=None,
                 offsets=None,
                 offset_transform=None,
                 norm=None,  # optional for ScalarMappable
                 cmap=None,  # ditto
                 pickradius=5.0,
                 hatch=None,
                 urls=None,
                 *,
                 zorder=1,
                 **kwargs
                 ):
        """
        Parameters
        ----------
        edgecolors : color or list of colors, default: :rc:`patch.edgecolor`
            Edge color for each patch making up the collection. The special
            value 'face' can be passed to make the edgecolor match the
            facecolor.
        facecolors : color or list of colors, default: :rc:`patch.facecolor`
            Face color for each patch making up the collection.
        linewidths : float or list of floats, default: :rc:`patch.linewidth`
            Line width for each patch making up the collection.
        linestyles : str or tuple or list thereof, default: 'solid'
            Valid strings are ['solid', 'dashed', 'dashdot', 'dotted', '-',
            '--', '-.', ':']. Dash tuples should be of the form::

                (offset, onoffseq),

            where *onoffseq* is an even length tuple of on and off ink lengths
            in points. For examples, see
            :doc:`/gallery/lines_bars_and_markers/linestyles`.
        capstyle : `.CapStyle`-like, default: :rc:`patch.capstyle`
            Style to use for capping lines for all paths in the collection.
            Allowed values are %(CapStyle)s.
        joinstyle : `.JoinStyle`-like, default: :rc:`patch.joinstyle`
            Style to use for joining lines for all paths in the collection.
            Allowed values are %(JoinStyle)s.
        antialiaseds : bool or list of bool, default: :rc:`patch.antialiased`
            Whether each patch in the collection should be drawn with
            antialiasing.
        offsets : (float, float) or list thereof, default: (0, 0)
            A vector by which to translate each patch after rendering (default
            is no translation). The translation is performed in screen (pixel)
            coordinates (i.e. after the Artist's transform is applied).
        offset_transform : `~.Transform`, default: `.IdentityTransform`
            A single transform which will be applied to each *offsets* vector
            before it is used.
        cmap, norm
            Data normalization and colormapping parameters. See
            `.ScalarMappable` for a detailed description.
        hatch : str, optional
            Hatching pattern to use in filled paths, if any. Valid strings are
            ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']. See
            :doc:`/gallery/shapes_and_collections/hatch_style_reference` for
            the meaning of each hatch type.
        pickradius : float, default: 5.0
            If ``pickradius <= 0``, then `.Collection.contains` will return
            ``True`` whenever the test point is inside of one of the polygons
            formed by the control points of a Path in the Collection. On the
            other hand, if it is greater than 0, then we instead check if the
            test point is contained in a stroke of width ``2*pickradius``
            following any of the Paths in the Collection.
        urls : list of str, default: None
            A URL for each patch to link to once drawn. Currently only works
            for the SVG backend. See :doc:`/gallery/misc/hyperlinks_sgskip` for
            examples.
        zorder : float, default: 1
            The drawing order, shared by all Patches in the Collection. See
            :doc:`/gallery/misc/zorder_demo` for all defaults and examples.
        """
        artist.Artist.__init__(self)
        cm.ScalarMappable.__init__(self, norm, cmap)
        # list of un-scaled dash patterns
        # this is needed scaling the dash pattern by linewidth
        self._us_linestyles = [(0, None)]
        # list of dash patterns
        self._linestyles = [(0, None)]
        # list of unbroadcast/scaled linewidths
        self._us_lw = [0]
        self._linewidths = [0]
        # Flags set by _set_mappable_flags: are colors from mapping an array?
        self._face_is_mapped = None
        self._edge_is_mapped = None
        self._mapped_colors = None  # calculated in update_scalarmappable
        self._hatch_color = mcolors.to_rgba(mpl.rcParams['hatch.color'])
        self.set_facecolor(facecolors)
        self.set_edgecolor(edgecolors)
        self.set_linewidth(linewidths)
        self.set_linestyle(linestyles)
        self.set_antialiased(antialiaseds)
        self.set_pickradius(pickradius)
        self.set_urls(urls)
        self.set_hatch(hatch)
        self.set_zorder(zorder)

        if capstyle:
            self.set_capstyle(capstyle)
        else:
            self._capstyle = None

        if joinstyle:
            self.set_joinstyle(joinstyle)
        else:
            self._joinstyle = None

        if offsets is not None:
            offsets = np.asanyarray(offsets, float)
            # Broadcast (2,) -> (1, 2) but nothing else.
            if offsets.shape == (2,):
                offsets = offsets[None, :]

        self._offsets = offsets
        self._offset_transform = offset_transform

        self._path_effects = None
        self._internal_update(kwargs)
        self._paths = None

    def get_paths(self):
        return self._paths

    def set_paths(self, paths):
        raise NotImplementedError

    def get_transforms(self):
        return self._transforms

    def get_offset_transform(self):
        """Return the `.Transform` instance used by this artist offset."""
        if self._offset_transform is None:
            self._offset_transform = transforms.IdentityTransform()
        elif (not isinstance(self._offset_transform, transforms.Transform)
              and hasattr(self._offset_transform, '_as_mpl_transform')):
            self._offset_transform = \
                self._offset_transform._as_mpl_transform(self.axes)
        return self._offset_transform

    @_api.rename_parameter("3.6", "transOffset", "offset_transform")
    def set_offset_transform(self, offset_transform):
        """
        Set the artist offset transform.

        Parameters
        ----------
        offset_transform : `.Transform`
        """
        self._offset_transform = offset_transform

    def get_datalim(self, transData):
        # Calculate the data limits and return them as a `.Bbox`.
        #
        # This operation depends on the transforms for the data in the
        # collection and whether the collection has offsets:
        #
        # 1. offsets = None, transform child of transData: use the paths for
        # the automatic limits (i.e. for LineCollection in streamline).
        # 2. offsets != None: offset_transform is child of transData:
        #
        #    a. transform is child of transData: use the path + offset for
        #       limits (i.e for bar).
        #    b. transform is not a child of transData: just use the offsets
        #       for the limits (i.e. for scatter)
        #
        # 3. otherwise return a null Bbox.

        transform = self.get_transform()
        offset_trf = self.get_offset_transform()
        if not (isinstance(offset_trf, transforms.IdentityTransform)
                or offset_trf.contains_branch(transData)):
            # if the offsets are in some coords other than data,
            # then don't use them for autoscaling.
            return transforms.Bbox.null()
        offsets = self.get_offsets()

        paths = self.get_paths()
        if not len(paths):
            # No paths to transform
            return transforms.Bbox.null()

        if not transform.is_affine:
            paths = [transform.transform_path_non_affine(p) for p in paths]
            # Don't convert transform to transform.get_affine() here because
            # we may have transform.contains_branch(transData) but not
            # transforms.get_affine().contains_branch(transData).  But later,
            # be careful to only apply the affine part that remains.

        if any(transform.contains_branch_seperately(transData)):
            # collections that are just in data units (like quiver)
            # can properly have the axes limits set by their shape +
            # offset.  LineCollections that have no offsets can
            # also use this algorithm (like streamplot).
            if isinstance(offsets, np.ma.MaskedArray):
                offsets = offsets.filled(np.nan)
                # get_path_collection_extents handles nan but not masked arrays
            return mpath.get_path_collection_extents(
                transform.get_affine() - transData, paths,
                self.get_transforms(),
                offset_trf.transform_non_affine(offsets),
                offset_trf.get_affine().frozen())

        # NOTE: None is the default case where no offsets were passed in
        if self._offsets is not None:
            # this is for collections that have their paths (shapes)
            # in physical, axes-relative, or figure-relative units
            # (i.e. like scatter). We can't uniquely set limits based on
            # those shapes, so we just set the limits based on their
            # location.
            offsets = (offset_trf - transData).transform(offsets)
            # note A-B means A B^{-1}
            offsets = np.ma.masked_invalid(offsets)
            if not offsets.mask.all():
                bbox = transforms.Bbox.null()
                bbox.update_from_data_xy(offsets)
                return bbox
        return transforms.Bbox.null()

    def get_window_extent(self, renderer=None):
        # TODO: check to ensure that this does not fail for
        # cases other than scatter plot legend
        return self.get_datalim(transforms.IdentityTransform())

    def _prepare_points(self):
        # Helper for drawing and hit testing.

        transform = self.get_transform()
        offset_trf = self.get_offset_transform()
        offsets = self.get_offsets()
        paths = self.get_paths()

        if self.have_units():
            paths = []
            for path in self.get_paths():
                vertices = path.vertices
                xs, ys = vertices[:, 0], vertices[:, 1]
                xs = self.convert_xunits(xs)
                ys = self.convert_yunits(ys)
                paths.append(mpath.Path(np.column_stack([xs, ys]), path.codes))
            xs = self.convert_xunits(offsets[:, 0])
            ys = self.convert_yunits(offsets[:, 1])
            offsets = np.column_stack([xs, ys])

        if not transform.is_affine:
            paths = [transform.transform_path_non_affine(path)
                     for path in paths]
            transform = transform.get_affine()
        if not offset_trf.is_affine:
            offsets = offset_trf.transform_non_affine(offsets)
            # This might have changed an ndarray into a masked array.
            offset_trf = offset_trf.get_affine()

        if isinstance(offsets, np.ma.MaskedArray):
            offsets = offsets.filled(np.nan)
            # Changing from a masked array to nan-filled ndarray
            # is probably most efficient at this point.

        return transform, offset_trf, offsets, paths

    @artist.allow_rasterization
    def draw(self, renderer):
        if not self.get_visible():
            return
        renderer.open_group(self.__class__.__name__, self.get_gid())

        self.update_scalarmappable()

        transform, offset_trf, offsets, paths = self._prepare_points()

        gc = renderer.new_gc()
        self._set_gc_clip(gc)
        gc.set_snap(self.get_snap())

        if self._hatch:
            gc.set_hatch(self._hatch)
            gc.set_hatch_color(self._hatch_color)

        if self.get_sketch_params() is not None:
            gc.set_sketch_params(*self.get_sketch_params())

        if self.get_path_effects():
            from matplotlib.patheffects import PathEffectRenderer
            renderer = PathEffectRenderer(self.get_path_effects(), renderer)

        # If the collection is made up of a single shape/color/stroke,
        # it can be rendered once and blitted multiple times, using
        # `draw_markers` rather than `draw_path_collection`.  This is
        # *much* faster for Agg, and results in smaller file sizes in
        # PDF/SVG/PS.

        trans = self.get_transforms()
        facecolors = self.get_facecolor()
        edgecolors = self.get_edgecolor()
        do_single_path_optimization = False
        if (len(paths) == 1 and len(trans) <= 1 and
                len(facecolors) == 1 and len(edgecolors) == 1 and
                len(self._linewidths) == 1 and
                all(ls[1] is None for ls in self._linestyles) and
                len(self._antialiaseds) == 1 and len(self._urls) == 1 and
                self.get_hatch() is None):
            if len(trans):
                combined_transform = transforms.Affine2D(trans[0]) + transform
            else:
                combined_transform = transform
            extents = paths[0].get_extents(combined_transform)
            if (extents.width < self.figure.bbox.width
                    and extents.height < self.figure.bbox.height):
                do_single_path_optimization = True

        if self._joinstyle:
            gc.set_joinstyle(self._joinstyle)

        if self._capstyle:
            gc.set_capstyle(self._capstyle)

        if do_single_path_optimization:
            gc.set_foreground(tuple(edgecolors[0]))
            gc.set_linewidth(self._linewidths[0])
            gc.set_dashes(*self._linestyles[0])
            gc.set_antialiased(self._antialiaseds[0])
            gc.set_url(self._urls[0])
            renderer.draw_markers(
                gc, paths[0], combined_transform.frozen(),
                mpath.Path(offsets), offset_trf, tuple(facecolors[0]))
        else:
            renderer.draw_path_collection(
                gc, transform.frozen(), paths,
                self.get_transforms(), offsets, offset_trf,
                self.get_facecolor(), self.get_edgecolor(),
                self._linewidths, self._linestyles,
                self._antialiaseds, self._urls,
                "screen")  # offset_position, kept for backcompat.

        gc.restore()
        renderer.close_group(self.__class__.__name__)
        self.stale = False

    @_api.rename_parameter("3.6", "pr", "pickradius")
    def set_pickradius(self, pickradius):
        """
        Set the pick radius used for containment tests.

        Parameters
        ----------
        pickradius : float
            Pick radius, in points.
        """
        self._pickradius = pickradius

    def get_pickradius(self):
        return self._pickradius

    def contains(self, mouseevent):
        """
        Test whether the mouse event occurred in the collection.

        Returns ``bool, dict(ind=itemlist)``, where every item in itemlist
        contains the event.
        """
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info

        if not self.get_visible():
            return False, {}

        pickradius = (
            float(self._picker)
            if isinstance(self._picker, Number) and
               self._picker is not True  # the bool, not just nonzero or 1
            else self._pickradius)

        if self.axes:
            self.axes._unstale_viewLim()

        transform, offset_trf, offsets, paths = self._prepare_points()

        # Tests if the point is contained on one of the polygons formed
        # by the control points of each of the paths. A point is considered
        # "on" a path if it would lie within a stroke of width 2*pickradius
        # following the path. If pickradius <= 0, then we instead simply check
        # if the point is *inside* of the path instead.
        ind = _path.point_in_path_collection(
            mouseevent.x, mouseevent.y, pickradius,
            transform.frozen(), paths, self.get_transforms(),
            offsets, offset_trf, pickradius <= 0)

        return len(ind) > 0, dict(ind=ind)

    def set_urls(self, urls):
        """
        Parameters
        ----------
        urls : list of str or None

        Notes
        -----
        URLs are currently only implemented by the SVG backend. They are
        ignored by all other backends.
        """
        self._urls = urls if urls is not None else [None]
        self.stale = True

    def get_urls(self):
        """
        Return a list of URLs, one for each element of the collection.

        The list contains *None* for elements without a URL. See
        :doc:`/gallery/misc/hyperlinks_sgskip` for an example.
        """
        return self._urls

    def set_hatch(self, hatch):
        r"""
        Set the hatching pattern

        *hatch* can be one of::

          /   - diagonal hatching
          \   - back diagonal
          |   - vertical
          -   - horizontal
          +   - crossed
          x   - crossed diagonal
          o   - small circle
          O   - large circle
          .   - dots
          *   - stars

        Letters can be combined, in which case all the specified
        hatchings are done.  If same letter repeats, it increases the
        density of hatching of that pattern.

        Hatching is supported in the PostScript, PDF, SVG and Agg
        backends only.

        Unlike other properties such as linewidth and colors, hatching
        can only be specified for the collection as a whole, not separately
        for each member.

        Parameters
        ----------
        hatch : {'/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}
        """
        # Use validate_hatch(list) after deprecation.
        mhatch._validate_hatch_pattern(hatch)
        self._hatch = hatch
        self.stale = True

    def get_hatch(self):
        """Return the current hatching pattern."""
        return self._hatch

    def set_offsets(self, offsets):
        """
        Set the offsets for the collection.

        Parameters
        ----------
        offsets : (N, 2) or (2,) array-like
        """
        offsets = np.asanyarray(offsets)
        if offsets.shape == (2,):  # Broadcast (2,) -> (1, 2) but nothing else.
            offsets = offsets[None, :]
        self._offsets = np.column_stack(
            (np.asarray(self.convert_xunits(offsets[:, 0]), 'float'),
             np.asarray(self.convert_yunits(offsets[:, 1]), 'float')))
        self.stale = True

    def get_offsets(self):
        """Return the offsets for the collection."""
        # Default to zeros in the no-offset (None) case
        return np.zeros((1, 2)) if self._offsets is None else self._offsets

    def _get_default_linewidth(self):
        # This may be overridden in a subclass.
        return mpl.rcParams['patch.linewidth']  # validated as float

    def set_linewidth(self, lw):
        """
        Set the linewidth(s) for the collection.  *lw* can be a scalar
        or a sequence; if it is a sequence the patches will cycle
        through the sequence

        Parameters
        ----------
        lw : float or list of floats
        """
        if lw is None:
            lw = self._get_default_linewidth()
        # get the un-scaled/broadcast lw
        self._us_lw = np.atleast_1d(np.asarray(lw))

        # scale all of the dash patterns.
        self._linewidths, self._linestyles = self._bcast_lwls(
            self._us_lw, self._us_linestyles)
        self.stale = True

    def set_linestyle(self, ls):
        """
        Set the linestyle(s) for the collection.

        ===========================   =================
        linestyle                     description
        ===========================   =================
        ``'-'`` or ``'solid'``        solid line
        ``'--'`` or  ``'dashed'``     dashed line
        ``'-.'`` or  ``'dashdot'``    dash-dotted line
        ``':'`` or ``'dotted'``       dotted line
        ===========================   =================

        Alternatively a dash tuple of the following form can be provided::

            (offset, onoffseq),

        where ``onoffseq`` is an even length tuple of on and off ink in points.

        Parameters
        ----------
        ls : str or tuple or list thereof
            Valid values for individual linestyles include {'-', '--', '-.',
            ':', '', (offset, on-off-seq)}. See `.Line2D.set_linestyle` for a
            complete description.
        """
        try:
            if isinstance(ls, str):
                ls = cbook.ls_mapper.get(ls, ls)
                dashes = [mlines._get_dash_pattern(ls)]
            else:
                try:
                    dashes = [mlines._get_dash_pattern(ls)]
                except ValueError:
                    dashes = [mlines._get_dash_pattern(x) for x in ls]

        except ValueError as err:
            raise ValueError('Do not know how to convert {!r} to '
                             'dashes'.format(ls)) from err

        # get the list of raw 'unscaled' dash patterns
        self._us_linestyles = dashes

        # broadcast and scale the lw and dash patterns
        self._linewidths, self._linestyles = self._bcast_lwls(
            self._us_lw, self._us_linestyles)

    @_docstring.interpd
    def set_capstyle(self, cs):
        """
        Set the `.CapStyle` for the collection (for all its elements).

        Parameters
        ----------
        cs : `.CapStyle` or %(CapStyle)s
        """
        self._capstyle = CapStyle(cs)

    def get_capstyle(self):
        return self._capstyle.name

    @_docstring.interpd
    def set_joinstyle(self, js):
        """
        Set the `.JoinStyle` for the collection (for all its elements).

        Parameters
        ----------
        js : `.JoinStyle` or %(JoinStyle)s
        """
        self._joinstyle = JoinStyle(js)

    def get_joinstyle(self):
        return self._joinstyle.name

    @staticmethod
    def _bcast_lwls(linewidths, dashes):
        """
        Internal helper function to broadcast + scale ls/lw

        In the collection drawing code, the linewidth and linestyle are cycled
        through as circular buffers (via ``v[i % len(v)]``).  Thus, if we are
        going to scale the dash pattern at set time (not draw time) we need to
        do the broadcasting now and expand both lists to be the same length.

        Parameters
        ----------
        linewidths : list
            line widths of collection
        dashes : list
            dash specification (offset, (dash pattern tuple))

        Returns
        -------
        linewidths, dashes : list
            Will be the same length, dashes are scaled by paired linewidth
        """
        if mpl.rcParams['_internal.classic_mode']:
            return linewidths, dashes
        # make sure they are the same length so we can zip them
        if len(dashes) != len(linewidths):
            l_dashes = len(dashes)
            l_lw = len(linewidths)
            gcd = math.gcd(l_dashes, l_lw)
            dashes = list(dashes) * (l_lw // gcd)
            linewidths = list(linewidths) * (l_dashes // gcd)

        # scale the dash patterns
        dashes = [mlines._scale_dashes(o, d, lw)
                  for (o, d), lw in zip(dashes, linewidths)]

        return linewidths, dashes

    def set_antialiased(self, aa):
        """
        Set the antialiasing state for rendering.

        Parameters
        ----------
        aa : bool or list of bools
        """
        if aa is None:
            aa = self._get_default_antialiased()
        self._antialiaseds = np.atleast_1d(np.asarray(aa, bool))
        self.stale = True

    def _get_default_antialiased(self):
        # This may be overridden in a subclass.
        return mpl.rcParams['patch.antialiased']

    def set_color(self, c):
        """
        Set both the edgecolor and the facecolor.

        Parameters
        ----------
        c : color or list of rgba tuples

        See Also
        --------
        Collection.set_facecolor, Collection.set_edgecolor
            For setting the edge or face color individually.
        """
        self.set_facecolor(c)
        self.set_edgecolor(c)

    def _get_default_facecolor(self):
        # This may be overridden in a subclass.
        return mpl.rcParams['patch.facecolor']

    def _set_facecolor(self, c):
        if c is None:
            c = self._get_default_facecolor()

        self._facecolors = mcolors.to_rgba_array(c, self._alpha)
        self.stale = True

    def set_facecolor(self, c):
        """
        Set the facecolor(s) of the collection. *c* can be a color (all patches
        have same color), or a sequence of colors; if it is a sequence the
        patches will cycle through the sequence.

        If *c* is 'none', the patch will not be filled.

        Parameters
        ----------
        c : color or list of colors
        """
        if isinstance(c, str) and c.lower() in ("none", "face"):
            c = c.lower()
        self._original_facecolor = c
        self._set_facecolor(c)

    def get_facecolor(self):
        return self._facecolors

    def get_edgecolor(self):
        if cbook._str_equal(self._edgecolors, 'face'):
            return self.get_facecolor()
        else:
            return self._edgecolors

    def _get_default_edgecolor(self):
        # This may be overridden in a subclass.
        return mpl.rcParams['patch.edgecolor']

    def _set_edgecolor(self, c):
        set_hatch_color = True
        if c is None:
            if (mpl.rcParams['patch.force_edgecolor']
                    or self._edge_default
                    or cbook._str_equal(self._original_facecolor, 'none')):
                c = self._get_default_edgecolor()
            else:
                c = 'none'
                set_hatch_color = False
        if cbook._str_lower_equal(c, 'face'):
            self._edgecolors = 'face'
            self.stale = True
            return
        self._edgecolors = mcolors.to_rgba_array(c, self._alpha)
        if set_hatch_color and len(self._edgecolors):
            self._hatch_color = tuple(self._edgecolors[0])
        self.stale = True

    def set_edgecolor(self, c):
        """
        Set the edgecolor(s) of the collection.

        Parameters
        ----------
        c : color or list of colors or 'face'
            The collection edgecolor(s).  If a sequence, the patches cycle
            through it.  If 'face', match the facecolor.
        """
        # We pass through a default value for use in LineCollection.
        # This allows us to maintain None as the default indicator in
        # _original_edgecolor.
        if isinstance(c, str) and c.lower() in ("none", "face"):
            c = c.lower()
        self._original_edgecolor = c
        self._set_edgecolor(c)

    def set_alpha(self, alpha):
        """
        Set the transparency of the collection.

        Parameters
        ----------
        alpha : float or array of float or None
            If not None, *alpha* values must be between 0 and 1, inclusive.
            If an array is provided, its length must match the number of
            elements in the collection.  Masked values and nans are not
            supported.
        """
        artist.Artist._set_alpha_for_array(self, alpha)
        self._set_facecolor(self._original_facecolor)
        self._set_edgecolor(self._original_edgecolor)

    set_alpha.__doc__ = artist.Artist._set_alpha_for_array.__doc__

    def get_linewidth(self):
        return self._linewidths

    def get_linestyle(self):
        return self._linestyles

    def _set_mappable_flags(self):
        """
        Determine whether edges and/or faces are color-mapped.

        This is a helper for update_scalarmappable.
        It sets Boolean flags '_edge_is_mapped' and '_face_is_mapped'.

        Returns
        -------
        mapping_change : bool
            True if either flag is True, or if a flag has changed.
        """
        # The flags are initialized to None to ensure this returns True
        # the first time it is called.
        edge0 = self._edge_is_mapped
        face0 = self._face_is_mapped
        # After returning, the flags must be Booleans, not None.
        self._edge_is_mapped = False
        self._face_is_mapped = False
        if self._A is not None:
            if not cbook._str_equal(self._original_facecolor, 'none'):
                self._face_is_mapped = True
                if cbook._str_equal(self._original_edgecolor, 'face'):
                    self._edge_is_mapped = True
            else:
                if self._original_edgecolor is None:
                    self._edge_is_mapped = True

        mapped = self._face_is_mapped or self._edge_is_mapped
        changed = (edge0 is None or face0 is None
                   or self._edge_is_mapped != edge0
                   or self._face_is_mapped != face0)
        return mapped or changed

    def update_scalarmappable(self):
        """
        Update colors from the scalar mappable array, if any.

        Assign colors to edges and faces based on the array and/or
        colors that were directly set, as appropriate.
        """
        if not self._set_mappable_flags():
            return
        # Allow possibility to call 'self.set_array(None)'.
        if self._A is not None:
            # QuadMesh can map 2d arrays (but pcolormesh supplies 1d array)
            if self._A.ndim > 1 and not isinstance(self, QuadMesh):
                raise ValueError('Collections can only map rank 1 arrays')
            if np.iterable(self._alpha):
                if self._alpha.size != self._A.size:
                    raise ValueError(
                        f'Data array shape, {self._A.shape} '
                        'is incompatible with alpha array shape, '
                        f'{self._alpha.shape}. '
                        'This can occur with the deprecated '
                        'behavior of the "flat" shading option, '
                        'in which a row and/or column of the data '
                        'array is dropped.')
                # pcolormesh, scatter, maybe others flatten their _A
                self._alpha = self._alpha.reshape(self._A.shape)
            self._mapped_colors = self.to_rgba(self._A, self._alpha)

        if self._face_is_mapped:
            self._facecolors = self._mapped_colors
        else:
            self._set_facecolor(self._original_facecolor)
        if self._edge_is_mapped:
            self._edgecolors = self._mapped_colors
        else:
            self._set_edgecolor(self._original_edgecolor)
        self.stale = True

    def get_fill(self):
        """Return whether face is colored."""
        return not cbook._str_lower_equal(self._original_facecolor, "none")

    def update_from(self, other):
        """Copy properties from other to self."""

        artist.Artist.update_from(self, other)
        self._antialiaseds = other._antialiaseds
        self._mapped_colors = other._mapped_colors
        self._edge_is_mapped = other._edge_is_mapped
        self._original_edgecolor = other._original_edgecolor
        self._edgecolors = other._edgecolors
        self._face_is_mapped = other._face_is_mapped
        self._original_facecolor = other._original_facecolor
        self._facecolors = other._facecolors
        self._linewidths = other._linewidths
        self._linestyles = other._linestyles
        self._us_linestyles = other._us_linestyles
        self._pickradius = other._pickradius
        self._hatch = other._hatch

        # update_from for scalarmappable
        self._A = other._A
        self.norm = other.norm
        self.cmap = other.cmap
        self.stale = True
