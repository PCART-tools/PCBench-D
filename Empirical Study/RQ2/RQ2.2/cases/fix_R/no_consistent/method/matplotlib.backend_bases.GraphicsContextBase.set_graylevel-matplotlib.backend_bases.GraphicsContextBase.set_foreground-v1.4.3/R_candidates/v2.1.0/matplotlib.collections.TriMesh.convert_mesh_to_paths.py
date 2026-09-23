    @staticmethod
    def convert_mesh_to_paths(tri):
        """
        Converts a given mesh into a sequence of
        :class:`matplotlib.path.Path` objects for easier rendering by
        backends that do not directly support meshes.

        This function is primarily of use to backend implementers.
        """
        Path = mpath.Path
        triangles = tri.get_masked_triangles()
        verts = np.concatenate((tri.x[triangles][..., np.newaxis],
                                tri.y[triangles][..., np.newaxis]), axis=2)
        return [Path(x) for x in verts]
