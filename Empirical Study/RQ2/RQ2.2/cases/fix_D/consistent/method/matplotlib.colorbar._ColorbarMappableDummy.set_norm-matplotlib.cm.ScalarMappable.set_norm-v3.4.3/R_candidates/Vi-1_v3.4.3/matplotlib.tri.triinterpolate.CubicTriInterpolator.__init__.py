    def __init__(self, triangulation, z, kind='min_E', trifinder=None,
                 dz=None):
        super().__init__(triangulation, z, trifinder)

        # Loads the underlying c++ _triangulation.
        # (During loading, reordering of triangulation._triangles may occur so
        # that all final triangles are now anti-clockwise)
        self._triangulation.get_cpp_triangulation()

        # To build the stiffness matrix and avoid zero-energy spurious modes
        # we will only store internally the valid (unmasked) triangles and
        # the necessary (used) points coordinates.
        # 2 renumbering tables need to be computed and stored:
        #  - a triangle renum table in order to translate the result from a
        #    TriFinder instance into the internal stored triangle number.
        #  - a node renum table to overwrite the self._z values into the new
        #    (used) node numbering.
        tri_analyzer = TriAnalyzer(self._triangulation)
        (compressed_triangles, compressed_x, compressed_y, tri_renum,
         node_renum) = tri_analyzer._get_compressed_triangulation()
        self._triangles = compressed_triangles
        self._tri_renum = tri_renum
        # Taking into account the node renumbering in self._z:
        valid_node = (node_renum != -1)
        self._z[node_renum[valid_node]] = self._z[valid_node]

        # Computing scale factors
        self._unit_x = np.ptp(compressed_x)
        self._unit_y = np.ptp(compressed_y)
        self._pts = np.column_stack([compressed_x / self._unit_x,
                                     compressed_y / self._unit_y])
        # Computing triangle points
        self._tris_pts = self._pts[self._triangles]
        # Computing eccentricities
        self._eccs = self._compute_tri_eccentricities(self._tris_pts)
        # Computing dof estimations for HCT triangle shape function
        self._dof = self._compute_dof(kind, dz=dz)
        # Loading HCT element
        self._ReferenceElement = _ReducedHCT_Element()
