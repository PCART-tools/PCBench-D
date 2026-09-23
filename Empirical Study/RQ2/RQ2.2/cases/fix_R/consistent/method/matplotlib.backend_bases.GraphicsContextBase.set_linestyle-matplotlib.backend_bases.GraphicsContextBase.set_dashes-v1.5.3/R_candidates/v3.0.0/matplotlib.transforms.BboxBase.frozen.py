    def frozen(self):
        return Bbox(self.get_points().copy())
