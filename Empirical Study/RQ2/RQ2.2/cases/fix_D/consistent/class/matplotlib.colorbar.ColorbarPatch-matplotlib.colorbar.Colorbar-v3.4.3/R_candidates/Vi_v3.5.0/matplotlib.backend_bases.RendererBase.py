class RendererBase:
    """
    An abstract base class to handle drawing/rendering operations.

    The following methods must be implemented in the backend for full
    functionality (though just implementing :meth:`draw_path` alone would
    give a highly capable backend):

    * :meth:`draw_path`
    * :meth:`draw_image`
    * :meth:`draw_gouraud_triangle`

    The following methods *should* be implemented in the backend for
    optimization reasons:

    * :meth:`draw_text`
    * :meth:`draw_markers`
    * :meth:`draw_path_collection`
    * :meth:`draw_quad_mesh`
    """

    def __init__(self):
        super().__init__()
        self._texmanager = None
        self._text2path = textpath.TextToPath()
        self._raster_depth = 0
        self._rasterizing = False

    def open_group(self, s, gid=None):
        """
        Open a grouping element with label *s* and *gid* (if set) as id.

        Only used by the SVG renderer.
        """

    def close_group(self, s):
        """
        Close a grouping element with label *s*.

        Only used by the SVG renderer.
        """

    def draw_path(self, gc, path, transform, rgbFace=None):
        """Draw a `~.path.Path` instance using the given affine transform."""
        raise NotImplementedError

    def draw_markers(self, gc, marker_path, marker_trans, path,
                     trans, rgbFace=None):
        """
        Draw a marker at each of *path*'s vertices (excluding control points).

        This provides a fallback implementation of draw_markers that
        makes multiple calls to :meth:`draw_path`.  Some backends may
        want to override this method in order to draw the marker only
        once and reuse it multiple times.

        Parameters
        ----------
        gc : `.GraphicsContextBase`
            The graphics context.
        marker_trans : `matplotlib.transforms.Transform`
            An affine transform applied to the marker.
        trans : `matplotlib.transforms.Transform`
            An affine transform applied to the path.
        """
        for vertices, codes in path.iter_segments(trans, simplify=False):
            if len(vertices):
                x, y = vertices[-2:]
                self.draw_path(gc, marker_path,
                               marker_trans +
                               transforms.Affine2D().translate(x, y),
                               rgbFace)

    def draw_path_collection(self, gc, master_transform, paths, all_transforms,
                             offsets, offsetTrans, facecolors, edgecolors,
                             linewidths, linestyles, antialiaseds, urls,
                             offset_position):
        """
        Draw a collection of paths selecting drawing properties from
        the lists *facecolors*, *edgecolors*, *linewidths*,
        *linestyles* and *antialiaseds*. *offsets* is a list of
        offsets to apply to each of the paths.  The offsets in
        *offsets* are first transformed by *offsetTrans* before being
        applied.

        *offset_position* is unused now, but the argument is kept for
        backwards compatibility.

        This provides a fallback implementation of
        :meth:`draw_path_collection` that makes multiple calls to
        :meth:`draw_path`.  Some backends may want to override this in
        order to render each set of path data only once, and then
        reference that path multiple times with the different offsets,
        colors, styles etc.  The generator methods
        :meth:`_iter_collection_raw_paths` and
        :meth:`_iter_collection` are provided to help with (and
        standardize) the implementation across backends.  It is highly
        recommended to use those generators, so that changes to the
        behavior of :meth:`draw_path_collection` can be made globally.
        """
        path_ids = self._iter_collection_raw_paths(master_transform,
                                                   paths, all_transforms)

        for xo, yo, path_id, gc0, rgbFace in self._iter_collection(
                gc, master_transform, all_transforms, list(path_ids), offsets,
                offsetTrans, facecolors, edgecolors, linewidths, linestyles,
                antialiaseds, urls, offset_position):
            path, transform = path_id
            # Only apply another translation if we have an offset, else we
            # reuse the initial transform.
            if xo != 0 or yo != 0:
                # The transformation can be used by multiple paths. Since
                # translate is a inplace operation, we need to copy the
                # transformation by .frozen() before applying the translation.
                transform = transform.frozen()
                transform.translate(xo, yo)
            self.draw_path(gc0, path, transform, rgbFace)

    def draw_quad_mesh(self, gc, master_transform, meshWidth, meshHeight,
                       coordinates, offsets, offsetTrans, facecolors,
                       antialiased, edgecolors):
        """
        Fallback implementation of :meth:`draw_quad_mesh` that generates paths
        and then calls :meth:`draw_path_collection`.
        """

        from matplotlib.collections import QuadMesh
        paths = QuadMesh._convert_mesh_to_paths(coordinates)

        if edgecolors is None:
            edgecolors = facecolors
        linewidths = np.array([gc.get_linewidth()], float)

        return self.draw_path_collection(
            gc, master_transform, paths, [], offsets, offsetTrans, facecolors,
            edgecolors, linewidths, [], [antialiased], [None], 'screen')

    def draw_gouraud_triangle(self, gc, points, colors, transform):
        """
        Draw a Gouraud-shaded triangle.

        Parameters
        ----------
        gc : `.GraphicsContextBase`
            The graphics context.
        points : (3, 2) array-like
            Array of (x, y) points for the triangle.
        colors : (3, 4) array-like
            RGBA colors for each point of the triangle.
        transform : `matplotlib.transforms.Transform`
            An affine transform to apply to the points.
        """
        raise NotImplementedError

    def draw_gouraud_triangles(self, gc, triangles_array, colors_array,
                               transform):
        """
        Draw a series of Gouraud triangles.

        Parameters
        ----------
        points : (N, 3, 2) array-like
            Array of *N* (x, y) points for the triangles.
        colors : (N, 3, 4) array-like
            Array of *N* RGBA colors for each point of the triangles.
        transform : `matplotlib.transforms.Transform`
            An affine transform to apply to the points.
        """
        transform = transform.frozen()
        for tri, col in zip(triangles_array, colors_array):
            self.draw_gouraud_triangle(gc, tri, col, transform)

    def _iter_collection_raw_paths(self, master_transform, paths,
                                   all_transforms):
        """
        Helper method (along with :meth:`_iter_collection`) to implement
        :meth:`draw_path_collection` in a space-efficient manner.

        This method yields all of the base path/transform
        combinations, given a master transform, a list of paths and
        list of transforms.

        The arguments should be exactly what is passed in to
        :meth:`draw_path_collection`.

        The backend should take each yielded path and transform and
        create an object that can be referenced (reused) later.
        """
        Npaths = len(paths)
        Ntransforms = len(all_transforms)
        N = max(Npaths, Ntransforms)

        if Npaths == 0:
            return

        transform = transforms.IdentityTransform()
        for i in range(N):
            path = paths[i % Npaths]
            if Ntransforms:
                transform = Affine2D(all_transforms[i % Ntransforms])
            yield path, transform + master_transform

    def _iter_collection_uses_per_path(self, paths, all_transforms,
                                       offsets, facecolors, edgecolors):
        """
        Compute how many times each raw path object returned by
        _iter_collection_raw_paths would be used when calling
        _iter_collection. This is intended for the backend to decide
        on the tradeoff between using the paths in-line and storing
        them once and reusing. Rounds up in case the number of uses
        is not the same for every path.
        """
        Npaths = len(paths)
        if Npaths == 0 or len(facecolors) == len(edgecolors) == 0:
            return 0
        Npath_ids = max(Npaths, len(all_transforms))
        N = max(Npath_ids, len(offsets))
        return (N + Npath_ids - 1) // Npath_ids

    def _iter_collection(self, gc, master_transform, all_transforms,
                         path_ids, offsets, offsetTrans, facecolors,
                         edgecolors, linewidths, linestyles,
                         antialiaseds, urls, offset_position):
        """
        Helper method (along with :meth:`_iter_collection_raw_paths`) to
        implement :meth:`draw_path_collection` in a space-efficient manner.

        This method yields all of the path, offset and graphics
        context combinations to draw the path collection.  The caller
        should already have looped over the results of
        :meth:`_iter_collection_raw_paths` to draw this collection.

        The arguments should be the same as that passed into
        :meth:`draw_path_collection`, with the exception of
        *path_ids*, which is a list of arbitrary objects that the
        backend will use to reference one of the paths created in the
        :meth:`_iter_collection_raw_paths` stage.

        Each yielded result is of the form::

           xo, yo, path_id, gc, rgbFace

        where *xo*, *yo* is an offset; *path_id* is one of the elements of
        *path_ids*; *gc* is a graphics context and *rgbFace* is a color to
        use for filling the path.
        """
        Ntransforms = len(all_transforms)
        Npaths = len(path_ids)
        Noffsets = len(offsets)
        N = max(Npaths, Noffsets)
        Nfacecolors = len(facecolors)
        Nedgecolors = len(edgecolors)
        Nlinewidths = len(linewidths)
        Nlinestyles = len(linestyles)
        Naa = len(antialiaseds)
        Nurls = len(urls)

        if (Nfacecolors == 0 and Nedgecolors == 0) or Npaths == 0:
            return
        if Noffsets:
            toffsets = offsetTrans.transform(offsets)

        gc0 = self.new_gc()
        gc0.copy_properties(gc)

        if Nfacecolors == 0:
            rgbFace = None

        if Nedgecolors == 0:
            gc0.set_linewidth(0.0)

        xo, yo = 0, 0
        for i in range(N):
            path_id = path_ids[i % Npaths]
            if Noffsets:
                xo, yo = toffsets[i % Noffsets]
            if not (np.isfinite(xo) and np.isfinite(yo)):
                continue
            if Nfacecolors:
                rgbFace = facecolors[i % Nfacecolors]
            if Nedgecolors:
                if Nlinewidths:
                    gc0.set_linewidth(linewidths[i % Nlinewidths])
                if Nlinestyles:
                    gc0.set_dashes(*linestyles[i % Nlinestyles])
                fg = edgecolors[i % Nedgecolors]
                if len(fg) == 4:
                    if fg[3] == 0.0:
                        gc0.set_linewidth(0)
                    else:
                        gc0.set_foreground(fg)
                else:
                    gc0.set_foreground(fg)
            if rgbFace is not None and len(rgbFace) == 4:
                if rgbFace[3] == 0:
                    rgbFace = None
            gc0.set_antialiased(antialiaseds[i % Naa])
            if Nurls:
                gc0.set_url(urls[i % Nurls])

            yield xo, yo, path_id, gc0, rgbFace
        gc0.restore()

    def get_image_magnification(self):
        """
        Get the factor by which to magnify images passed to :meth:`draw_image`.
        Allows a backend to have images at a different resolution to other
        artists.
        """
        return 1.0

    def draw_image(self, gc, x, y, im, transform=None):
        """
        Draw an RGBA image.

        Parameters
        ----------
        gc : `.GraphicsContextBase`
            A graphics context with clipping information.

        x : scalar
            The distance in physical units (i.e., dots or pixels) from the left
            hand side of the canvas.

        y : scalar
            The distance in physical units (i.e., dots or pixels) from the
            bottom side of the canvas.

        im : (N, M, 4) array-like of np.uint8
            An array of RGBA pixels.

        transform : `matplotlib.transforms.Affine2DBase`
            If and only if the concrete backend is written such that
            :meth:`option_scale_image` returns ``True``, an affine
            transformation (i.e., an `.Affine2DBase`) *may* be passed to
            :meth:`draw_image`.  The translation vector of the transformation
            is given in physical units (i.e., dots or pixels). Note that
            the transformation does not override *x* and *y*, and has to be
            applied *before* translating the result by *x* and *y* (this can
            be accomplished by adding *x* and *y* to the translation vector
            defined by *transform*).
        """
        raise NotImplementedError

    def option_image_nocomposite(self):
        """
        Return whether image composition by Matplotlib should be skipped.

        Raster backends should usually return False (letting the C-level
        rasterizer take care of image composition); vector backends should
        usually return ``not rcParams["image.composite_image"]``.
        """
        return False

    def option_scale_image(self):
        """
        Return whether arbitrary affine transformations in :meth:`draw_image`
        are supported (True for most vector backends).
        """
        return False

    def draw_tex(self, gc, x, y, s, prop, angle, *, mtext=None):
        """
        """
        self._draw_text_as_path(gc, x, y, s, prop, angle, ismath="TeX")

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        """
        Draw the text instance.

        Parameters
        ----------
        gc : `.GraphicsContextBase`
            The graphics context.
        x : float
            The x location of the text in display coords.
        y : float
            The y location of the text baseline in display coords.
        s : str
            The text string.
        prop : `matplotlib.font_manager.FontProperties`
            The font properties.
        angle : float
            The rotation angle in degrees anti-clockwise.
        mtext : `matplotlib.text.Text`
            The original text object to be rendered.

        Notes
        -----
        **Note for backend implementers:**

        When you are trying to determine if you have gotten your bounding box
        right (which is what enables the text layout/alignment to work
        properly), it helps to change the line in text.py::

            if 0: bbox_artist(self, renderer)

        to if 1, and then the actual bounding box will be plotted along with
        your text.
        """

        self._draw_text_as_path(gc, x, y, s, prop, angle, ismath)

    def _get_text_path_transform(self, x, y, s, prop, angle, ismath):
        """
        Return the text path and transform.

        Parameters
        ----------
        prop : `matplotlib.font_manager.FontProperties`
            The font property.
        s : str
            The text to be converted.
        ismath : bool or "TeX"
            If True, use mathtext parser. If "TeX", use *usetex* mode.
        """

        text2path = self._text2path
        fontsize = self.points_to_pixels(prop.get_size_in_points())
        verts, codes = text2path.get_text_path(prop, s, ismath=ismath)

        path = Path(verts, codes)
        angle = np.deg2rad(angle)
        if self.flipy():
            width, height = self.get_canvas_width_height()
            transform = (Affine2D()
                         .scale(fontsize / text2path.FONT_SCALE)
                         .rotate(angle)
                         .translate(x, height - y))
        else:
            transform = (Affine2D()
                         .scale(fontsize / text2path.FONT_SCALE)
                         .rotate(angle)
                         .translate(x, y))

        return path, transform

    def _draw_text_as_path(self, gc, x, y, s, prop, angle, ismath):
        """
        Draw the text by converting them to paths using textpath module.

        Parameters
        ----------
        prop : `matplotlib.font_manager.FontProperties`
            The font property.
        s : str
            The text to be converted.
        usetex : bool
            Whether to use usetex mode.
        ismath : bool or "TeX"
            If True, use mathtext parser. If "TeX", use *usetex* mode.
        """
        path, transform = self._get_text_path_transform(
            x, y, s, prop, angle, ismath)
        color = gc.get_rgb()
        gc.set_linewidth(0.0)
        self.draw_path(gc, path, transform, rgbFace=color)

    def get_text_width_height_descent(self, s, prop, ismath):
        """
        Get the width, height, and descent (offset from the bottom
        to the baseline), in display coords, of the string *s* with
        `.FontProperties` *prop*.
        """
        if ismath == 'TeX':
            # todo: handle props
            texmanager = self._text2path.get_texmanager()
            fontsize = prop.get_size_in_points()
            w, h, d = texmanager.get_text_width_height_descent(
                s, fontsize, renderer=self)
            return w, h, d

        dpi = self.points_to_pixels(72)
        if ismath:
            dims = self._text2path.mathtext_parser.parse(s, dpi, prop)
            return dims[0:3]  # return width, height, descent

        flags = self._text2path._get_hinting_flag()
        font = self._text2path._get_font(prop)
        size = prop.get_size_in_points()
        font.set_size(size, dpi)
        # the width and height of unrotated string
        font.set_text(s, 0.0, flags=flags)
        w, h = font.get_width_height()
        d = font.get_descent()
        w /= 64.0  # convert from subpixels
        h /= 64.0
        d /= 64.0
        return w, h, d

    def flipy(self):
        """
        Return whether y values increase from top to bottom.

        Note that this only affects drawing of texts and images.
        """
        return True

    def get_canvas_width_height(self):
        """Return the canvas width and height in display coords."""
        return 1, 1

    def get_texmanager(self):
        """Return the `.TexManager` instance."""
        if self._texmanager is None:
            from matplotlib.texmanager import TexManager
            self._texmanager = TexManager()
        return self._texmanager

    def new_gc(self):
        """Return an instance of a `.GraphicsContextBase`."""
        return GraphicsContextBase()

    def points_to_pixels(self, points):
        """
        Convert points to display units.

        You need to override this function (unless your backend
        doesn't have a dpi, e.g., postscript or svg).  Some imaging
        systems assume some value for pixels per inch::

            points to pixels = points * pixels_per_inch/72 * dpi/72

        Parameters
        ----------
        points : float or array-like
            a float or a numpy array of float

        Returns
        -------
        Points converted to pixels
        """
        return points

    def start_rasterizing(self):
        """
        Switch to the raster renderer.

        Used by `.MixedModeRenderer`.
        """

    def stop_rasterizing(self):
        """
        Switch back to the vector renderer and draw the contents of the raster
        renderer as an image on the vector renderer.

        Used by `.MixedModeRenderer`.
        """

    def start_filter(self):
        """
        Switch to a temporary renderer for image filtering effects.

        Currently only supported by the agg renderer.
        """

    def stop_filter(self, filter_func):
        """
        Switch back to the original renderer.  The contents of the temporary
        renderer is processed with the *filter_func* and is drawn on the
        original renderer as an image.

        Currently only supported by the agg renderer.
        """

    def _draw_disabled(self):
        """
        Context manager to temporary disable drawing.

        This is used for getting the drawn size of Artists.  This lets us
        run the draw process to update any Python state but does not pay the
        cost of the draw_XYZ calls on the canvas.
        """
        no_ops = {
            meth_name: lambda *args, **kwargs: None
            for meth_name in dir(RendererBase)
            if (meth_name.startswith("draw_")
                or meth_name in ["open_group", "close_group"])
        }

        return _setattr_cm(self, **no_ops)
