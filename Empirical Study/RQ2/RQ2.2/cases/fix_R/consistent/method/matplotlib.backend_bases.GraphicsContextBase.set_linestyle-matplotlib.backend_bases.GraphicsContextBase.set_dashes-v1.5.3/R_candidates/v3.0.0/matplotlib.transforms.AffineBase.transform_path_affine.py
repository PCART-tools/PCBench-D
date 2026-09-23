    def transform_path_affine(self, path):
        return Path(self.transform_affine(path.vertices),
                    path.codes, path._interpolation_steps)
