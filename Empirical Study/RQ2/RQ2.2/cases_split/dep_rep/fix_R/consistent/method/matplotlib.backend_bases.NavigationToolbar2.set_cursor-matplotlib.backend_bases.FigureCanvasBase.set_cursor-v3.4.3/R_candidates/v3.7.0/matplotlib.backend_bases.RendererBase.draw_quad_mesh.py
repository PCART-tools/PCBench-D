    def draw_quad_mesh(self, gc, master_transform, meshWidth, meshHeight,
                       coordinates, offsets, offsetTrans, facecolors,
                       antialiased, edgecolors):
        """
        Draw a quadmesh.

        The base (fallback) implementation converts the quadmesh to paths and
        then calls `draw_path_collection`.
        """

        from matplotlib.collections import QuadMesh
        paths = QuadMesh._convert_mesh_to_paths(coordinates)

        if edgecolors is None:
            edgecolors = facecolors
        linewidths = np.array([gc.get_linewidth()], float)

        return self.draw_path_collection(
            gc, master_transform, paths, [], offsets, offsetTrans, facecolors,
            edgecolors, linewidths, [], [antialiased], [None], 'screen')
