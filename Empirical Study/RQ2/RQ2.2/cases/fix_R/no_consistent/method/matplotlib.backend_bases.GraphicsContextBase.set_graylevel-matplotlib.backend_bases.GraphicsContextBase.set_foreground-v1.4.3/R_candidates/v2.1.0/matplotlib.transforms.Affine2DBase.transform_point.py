    def transform_point(self, point):
        mtx = self.get_matrix()
        return affine_transform([point], mtx)[0]
