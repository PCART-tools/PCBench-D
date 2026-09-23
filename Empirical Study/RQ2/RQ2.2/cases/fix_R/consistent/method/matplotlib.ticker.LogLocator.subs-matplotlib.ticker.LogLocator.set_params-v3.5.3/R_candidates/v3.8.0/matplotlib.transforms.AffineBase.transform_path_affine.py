    def transform_path_affine(self, path):
        # docstring inherited
        return Path(self.transform_affine(path.vertices),
                    path.codes, path._interpolation_steps)
