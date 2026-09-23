    @staticmethod
    def convert_mesh_to_paths(tri):
        """
        Converts a given mesh into a sequence of
        :class:`matplotlib.path.Path` objects for easier rendering by
        backends that do not directly support meshes.

        This function is primarily of use to backend implementers.
        """
        triangles = tri.get_masked_triangles()
        verts = np.stack((tri.x[triangles], tri.y[triangles]), axis=-1)
        return [mpath.Path(x) for x in verts]
