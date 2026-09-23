    def draw_quad_mesh(self, gc, master_transform, meshWidth, meshHeight,
                       coordinates, offsets, offsetTrans, facecolors,
                       antialiased, edgecolors):
        """
        This provides a fallback implementation of
        :meth:`draw_quad_mesh` that generates paths and then calls
        :meth:`draw_path_collection`.
        """

        from matplotlib.collections import QuadMesh
        paths = QuadMesh.convert_mesh_to_paths(
            meshWidth, meshHeight, coordinates)

        if edgecolors is None:
            edgecolors = facecolors
        linewidths = np.array([gc.get_linewidth()], float)

        return self.draw_path_collection(
            gc, master_transform, paths, [], offsets, offsetTrans, facecolors,
            edgecolors, linewidths, [], [antialiased], [None], 'screen')
