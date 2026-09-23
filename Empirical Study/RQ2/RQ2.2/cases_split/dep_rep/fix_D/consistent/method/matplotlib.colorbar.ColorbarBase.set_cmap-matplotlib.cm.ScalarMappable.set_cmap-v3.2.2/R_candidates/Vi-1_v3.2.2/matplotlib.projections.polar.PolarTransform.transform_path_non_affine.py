    def transform_path_non_affine(self, path):
        # docstring inherited
        vertices = path.vertices
        if len(vertices) == 2 and vertices[0, 0] == vertices[1, 0]:
            return mpath.Path(self.transform(vertices), path.codes)
        ipath = path.interpolated(path._interpolation_steps)
        return mpath.Path(self.transform(ipath.vertices), ipath.codes)
