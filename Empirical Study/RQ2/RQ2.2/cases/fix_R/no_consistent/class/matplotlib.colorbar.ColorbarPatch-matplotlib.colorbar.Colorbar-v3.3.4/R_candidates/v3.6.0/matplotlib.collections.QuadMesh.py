class QuadMesh(Collection):
    r"""
    Class for the efficient drawing of a quadrilateral mesh.

    A quadrilateral mesh is a grid of M by N adjacent quadrilaterals that are
    defined via a (M+1, N+1) grid of vertices. The quadrilateral (m, n) is
    defined by the vertices ::

               (m+1, n) ----------- (m+1, n+1)
                  /                   /
                 /                 /
                /               /
            (m, n) -------- (m, n+1)

    The mesh need not be regular and the polygons need not be convex.

    Parameters
    ----------
    coordinates : (M+1, N+1, 2) array-like
        The vertices. ``coordinates[m, n]`` specifies the (x, y) coordinates
        of vertex (m, n).

    antialiased : bool, default: True

    shading : {'flat', 'gouraud'}, default: 'flat'

    Notes
    -----
    Unlike other `.Collection`\s, the default *pickradius* of `.QuadMesh` is 0,
    i.e. `~.Artist.contains` checks whether the test point is within any of the
    mesh quadrilaterals.

    There exists a deprecated API version ``QuadMesh(M, N, coords)``, where
    the dimensions are given explicitly and ``coords`` is a (M*N, 2)
    array-like. This has been deprecated in Matplotlib 3.5. The following
    describes the semantics of this deprecated API.

    A quadrilateral mesh consists of a grid of vertices.
    The dimensions of this array are (*meshWidth* + 1, *meshHeight* + 1).
    Each vertex in the mesh has a different set of "mesh coordinates"
    representing its position in the topology of the mesh.
    For any values (*m*, *n*) such that 0 <= *m* <= *meshWidth*
    and 0 <= *n* <= *meshHeight*, the vertices at mesh coordinates
    (*m*, *n*), (*m*, *n* + 1), (*m* + 1, *n* + 1), and (*m* + 1, *n*)
    form one of the quadrilaterals in the mesh. There are thus
    (*meshWidth* * *meshHeight*) quadrilaterals in the mesh.  The mesh
    need not be regular and the polygons need not be convex.

    A quadrilateral mesh is represented by a (2 x ((*meshWidth* + 1) *
    (*meshHeight* + 1))) numpy array *coordinates*, where each row is
    the *x* and *y* coordinates of one of the vertices.  To define the
    function that maps from a data point to its corresponding color,
    use the :meth:`set_cmap` method.  Each of these arrays is indexed in
    row-major order by the mesh coordinates of the vertex (or the mesh
    coordinates of the lower left vertex, in the case of the colors).

    For example, the first entry in *coordinates* is the coordinates of the
    vertex at mesh coordinates (0, 0), then the one at (0, 1), then at (0, 2)
    .. (0, meshWidth), (1, 0), (1, 1), and so on.
    """

    def __init__(self, *args, **kwargs):
        # signature deprecation since="3.5": Change to new signature after the
        # deprecation has expired. Also remove setting __init__.__signature__,
        # and remove the Notes from the docstring.
        params = _api.select_matching_signature(
            [
                lambda meshWidth, meshHeight, coordinates, antialiased=True,
                       shading='flat', **kwargs: locals(),
                lambda coordinates, antialiased=True, shading='flat', **kwargs:
                       locals()
            ],
            *args, **kwargs).values()
        *old_w_h, coords, antialiased, shading, kwargs = params
        if old_w_h:  # The old signature matched.
            _api.warn_deprecated(
                "3.5",
                message="This usage of Quadmesh is deprecated: Parameters "
                        "meshWidth and meshHeights will be removed; "
                        "coordinates must be 2D; all parameters except "
                        "coordinates will be keyword-only.")
            w, h = old_w_h
            coords = np.asarray(coords, np.float64).reshape((h + 1, w + 1, 2))
        kwargs.setdefault("pickradius", 0)
        # end of signature deprecation code

        _api.check_shape((None, None, 2), coordinates=coords)
        self._coordinates = coords
        self._antialiased = antialiased
        self._shading = shading
        self._bbox = transforms.Bbox.unit()
        self._bbox.update_from_data_xy(self._coordinates.reshape(-1, 2))
        # super init delayed after own init because array kwarg requires
        # self._coordinates and self._shading
        super().__init__(**kwargs)
        self.set_mouseover(False)

    # Only needed during signature deprecation
    __init__.__signature__ = inspect.signature(
        lambda self, coordinates, *,
               antialiased=True, shading='flat', pickradius=0, **kwargs: None)

    def get_paths(self):
        if self._paths is None:
            self.set_paths()
        return self._paths

    def set_paths(self):
        self._paths = self._convert_mesh_to_paths(self._coordinates)
        self.stale = True

    def set_array(self, A):
        """
        Set the data values.

        Parameters
        ----------
        A : (M, N) array-like or M*N array-like
            If the values are provided as a 2D grid, the shape must match the
            coordinates grid. If the values are 1D, they are reshaped to 2D.
            M, N follow from the coordinates grid, where the coordinates grid
            shape is (M, N) for 'gouraud' *shading* and (M+1, N+1) for 'flat'
            shading.
        """
        height, width = self._coordinates.shape[0:-1]
        misshapen_data = False
        faulty_data = False

        if self._shading == 'flat':
            h, w = height-1, width-1
        else:
            h, w = height, width

        if A is not None:
            shape = np.shape(A)
            if len(shape) == 1:
                if shape[0] != (h*w):
                    faulty_data = True
            elif shape != (h, w):
                if np.prod(shape) == (h * w):
                    misshapen_data = True
                else:
                    faulty_data = True

            if misshapen_data:
                _api.warn_deprecated(
                    "3.5", message=f"For X ({width}) and Y ({height}) "
                    f"with {self._shading} shading, the expected shape of "
                    f"A is ({h}, {w}). Passing A ({A.shape}) is deprecated "
                    "since %(since)s and will become an error %(removal)s.")

            if faulty_data:
                raise TypeError(
                    f"Dimensions of A {A.shape} are incompatible with "
                    f"X ({width}) and/or Y ({height})")

        return super().set_array(A)

    def get_datalim(self, transData):
        return (self.get_transform() - transData).transform_bbox(self._bbox)

    def get_coordinates(self):
        """
        Return the vertices of the mesh as an (M+1, N+1, 2) array.

        M, N are the number of quadrilaterals in the rows / columns of the
        mesh, corresponding to (M+1, N+1) vertices.
        The last dimension specifies the components (x, y).
        """
        return self._coordinates

    @staticmethod
    @_api.deprecated("3.5", alternative="`QuadMesh(coordinates).get_paths()"
                     "<.QuadMesh.get_paths>`")
    def convert_mesh_to_paths(meshWidth, meshHeight, coordinates):
        return QuadMesh._convert_mesh_to_paths(coordinates)

    @staticmethod
    def _convert_mesh_to_paths(coordinates):
        """
        Convert a given mesh into a sequence of `.Path` objects.

        This function is primarily of use to implementers of backends that do
        not directly support quadmeshes.
        """
        if isinstance(coordinates, np.ma.MaskedArray):
            c = coordinates.data
        else:
            c = coordinates
        points = np.concatenate([
            c[:-1, :-1],
            c[:-1, 1:],
            c[1:, 1:],
            c[1:, :-1],
            c[:-1, :-1]
        ], axis=2).reshape((-1, 5, 2))
        return [mpath.Path(x) for x in points]

    @_api.deprecated("3.5")
    def convert_mesh_to_triangles(self, meshWidth, meshHeight, coordinates):
        return self._convert_mesh_to_triangles(coordinates)

    def _convert_mesh_to_triangles(self, coordinates):
        """
        Convert a given mesh into a sequence of triangles, each point
        with its own color.  The result can be used to construct a call to
        `~.RendererBase.draw_gouraud_triangle`.
        """
        if isinstance(coordinates, np.ma.MaskedArray):
            p = coordinates.data
        else:
            p = coordinates

        p_a = p[:-1, :-1]
        p_b = p[:-1, 1:]
        p_c = p[1:, 1:]
        p_d = p[1:, :-1]
        p_center = (p_a + p_b + p_c + p_d) / 4.0
        triangles = np.concatenate([
            p_a, p_b, p_center,
            p_b, p_c, p_center,
            p_c, p_d, p_center,
            p_d, p_a, p_center,
        ], axis=2).reshape((-1, 3, 2))

        c = self.get_facecolor().reshape((*coordinates.shape[:2], 4))
        c_a = c[:-1, :-1]
        c_b = c[:-1, 1:]
        c_c = c[1:, 1:]
        c_d = c[1:, :-1]
        c_center = (c_a + c_b + c_c + c_d) / 4.0
        colors = np.concatenate([
            c_a, c_b, c_center,
            c_b, c_c, c_center,
            c_c, c_d, c_center,
            c_d, c_a, c_center,
        ], axis=2).reshape((-1, 3, 4))

        return triangles, colors

    @artist.allow_rasterization
    def draw(self, renderer):
        if not self.get_visible():
            return
        renderer.open_group(self.__class__.__name__, self.get_gid())
        transform = self.get_transform()
        offset_trf = self.get_offset_transform()
        offsets = self.get_offsets()

        if self.have_units():
            xs = self.convert_xunits(offsets[:, 0])
            ys = self.convert_yunits(offsets[:, 1])
            offsets = np.column_stack([xs, ys])

        self.update_scalarmappable()

        if not transform.is_affine:
            coordinates = self._coordinates.reshape((-1, 2))
            coordinates = transform.transform(coordinates)
            coordinates = coordinates.reshape(self._coordinates.shape)
            transform = transforms.IdentityTransform()
        else:
            coordinates = self._coordinates

        if not offset_trf.is_affine:
            offsets = offset_trf.transform_non_affine(offsets)
            offset_trf = offset_trf.get_affine()

        gc = renderer.new_gc()
        gc.set_snap(self.get_snap())
        self._set_gc_clip(gc)
        gc.set_linewidth(self.get_linewidth()[0])

        if self._shading == 'gouraud':
            triangles, colors = self._convert_mesh_to_triangles(coordinates)
            renderer.draw_gouraud_triangles(
                gc, triangles, colors, transform.frozen())
        else:
            renderer.draw_quad_mesh(
                gc, transform.frozen(),
                coordinates.shape[1] - 1, coordinates.shape[0] - 1,
                coordinates, offsets, offset_trf,
                # Backends expect flattened rgba arrays (n*m, 4) for fc and ec
                self.get_facecolor().reshape((-1, 4)),
                self._antialiased, self.get_edgecolors().reshape((-1, 4)))
        gc.restore()
        renderer.close_group(self.__class__.__name__)
        self.stale = False

    def get_cursor_data(self, event):
        contained, info = self.contains(event)
        if contained and self.get_array() is not None:
            return self.get_array().ravel()[info["ind"]]
        return None
