class QuadMesh(Collection):
    """
    Class for the efficient drawing of a quadrilateral mesh.

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

    *shading* may be 'flat', or 'gouraud'
    """
    def __init__(self, meshWidth, meshHeight, coordinates,
                 antialiased=True, shading='flat', **kwargs):
        super().__init__(**kwargs)
        self._meshWidth = meshWidth
        self._meshHeight = meshHeight
        # By converting to floats now, we can avoid that on every draw.
        self._coordinates = np.asarray(coordinates, float).reshape(
            (meshHeight + 1, meshWidth + 1, 2))
        self._antialiased = antialiased
        self._shading = shading

        self._bbox = transforms.Bbox.unit()
        self._bbox.update_from_data_xy(coordinates.reshape(
            ((meshWidth + 1) * (meshHeight + 1), 2)))

    def get_paths(self):
        if self._paths is None:
            self.set_paths()
        return self._paths

    def set_paths(self):
        self._paths = self.convert_mesh_to_paths(
            self._meshWidth, self._meshHeight, self._coordinates)
        self.stale = True

    def get_datalim(self, transData):
        return (self.get_transform() - transData).transform_bbox(self._bbox)

    @staticmethod
    def convert_mesh_to_paths(meshWidth, meshHeight, coordinates):
        """
        Convert a given mesh into a sequence of `~.Path` objects.

        This function is primarily of use to implementers of backends that do
        not directly support quadmeshes.
        """
        if isinstance(coordinates, np.ma.MaskedArray):
            c = coordinates.data
        else:
            c = coordinates
        points = np.concatenate((
                    c[:-1, :-1],
                    c[:-1, 1:],
                    c[1:, 1:],
                    c[1:, :-1],
                    c[:-1, :-1]
                ), axis=2)
        points = points.reshape((meshWidth * meshHeight, 5, 2))
        return [mpath.Path(x) for x in points]

    def convert_mesh_to_triangles(self, meshWidth, meshHeight, coordinates):
        """
        Convert a given mesh into a sequence of triangles, each point
        with its own color.  This is useful for experiments using
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

        triangles = np.concatenate((
                p_a, p_b, p_center,
                p_b, p_c, p_center,
                p_c, p_d, p_center,
                p_d, p_a, p_center,
            ), axis=2)
        triangles = triangles.reshape((meshWidth * meshHeight * 4, 3, 2))

        c = self.get_facecolor().reshape((meshHeight + 1, meshWidth + 1, 4))
        c_a = c[:-1, :-1]
        c_b = c[:-1, 1:]
        c_c = c[1:, 1:]
        c_d = c[1:, :-1]
        c_center = (c_a + c_b + c_c + c_d) / 4.0

        colors = np.concatenate((
                        c_a, c_b, c_center,
                        c_b, c_c, c_center,
                        c_c, c_d, c_center,
                        c_d, c_a, c_center,
                    ), axis=2)
        colors = colors.reshape((meshWidth * meshHeight * 4, 3, 4))

        return triangles, colors

    @artist.allow_rasterization
    def draw(self, renderer):
        if not self.get_visible():
            return
        renderer.open_group(self.__class__.__name__, self.get_gid())
        transform = self.get_transform()
        transOffset = self.get_offset_transform()
        offsets = self._offsets

        if self.have_units():
            if len(self._offsets):
                xs = self.convert_xunits(self._offsets[:, 0])
                ys = self.convert_yunits(self._offsets[:, 1])
                offsets = np.column_stack([xs, ys])

        self.update_scalarmappable()

        if not transform.is_affine:
            coordinates = self._coordinates.reshape((-1, 2))
            coordinates = transform.transform(coordinates)
            coordinates = coordinates.reshape(self._coordinates.shape)
            transform = transforms.IdentityTransform()
        else:
            coordinates = self._coordinates

        if not transOffset.is_affine:
            offsets = transOffset.transform_non_affine(offsets)
            transOffset = transOffset.get_affine()

        gc = renderer.new_gc()
        gc.set_snap(self.get_snap())
        self._set_gc_clip(gc)
        gc.set_linewidth(self.get_linewidth()[0])

        if self._shading == 'gouraud':
            triangles, colors = self.convert_mesh_to_triangles(
                self._meshWidth, self._meshHeight, coordinates)
            renderer.draw_gouraud_triangles(
                gc, triangles, colors, transform.frozen())
        else:
            renderer.draw_quad_mesh(
                gc, transform.frozen(), self._meshWidth, self._meshHeight,
                coordinates, offsets, transOffset,
                # Backends expect flattened rgba arrays (n*m, 4) for fc and ec
                self.get_facecolor().reshape((-1, 4)),
                self._antialiased, self.get_edgecolors().reshape((-1, 4)))
        gc.restore()
        renderer.close_group(self.__class__.__name__)
        self.stale = False
