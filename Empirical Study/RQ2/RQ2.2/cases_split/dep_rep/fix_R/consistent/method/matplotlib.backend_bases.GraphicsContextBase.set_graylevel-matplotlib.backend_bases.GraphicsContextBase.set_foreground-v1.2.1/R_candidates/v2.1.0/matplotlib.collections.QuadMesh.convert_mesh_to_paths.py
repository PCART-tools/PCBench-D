    @staticmethod
    def convert_mesh_to_paths(meshWidth, meshHeight, coordinates):
        """
        Converts a given mesh into a sequence of
        :class:`matplotlib.path.Path` objects for easier rendering by
        backends that do not directly support quadmeshes.

        This function is primarily of use to backend implementers.
        """
        Path = mpath.Path

        if isinstance(coordinates, np.ma.MaskedArray):
            c = coordinates.data
        else:
            c = coordinates

        points = np.concatenate((
                    c[0:-1, 0:-1],
                    c[0:-1, 1:],
                    c[1:, 1:],
                    c[1:, 0:-1],
                    c[0:-1, 0:-1]
                ), axis=2)
        points = points.reshape((meshWidth * meshHeight, 5, 2))
        return [Path(x) for x in points]
