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
