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
