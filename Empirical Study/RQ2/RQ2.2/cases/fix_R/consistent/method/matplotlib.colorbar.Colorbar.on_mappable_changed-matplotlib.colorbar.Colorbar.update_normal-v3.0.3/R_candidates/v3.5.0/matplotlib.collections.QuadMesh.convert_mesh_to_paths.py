    @staticmethod
    @_api.deprecated("3.5", alternative="QuadMesh(coordinates).get_paths()")
    def convert_mesh_to_paths(meshWidth, meshHeight, coordinates):
        return QuadMesh._convert_mesh_to_paths(coordinates)
