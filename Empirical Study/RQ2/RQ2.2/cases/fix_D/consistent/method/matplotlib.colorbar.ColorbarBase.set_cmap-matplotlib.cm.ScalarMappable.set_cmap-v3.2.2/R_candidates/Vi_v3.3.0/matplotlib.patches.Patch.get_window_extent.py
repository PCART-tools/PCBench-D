    def get_window_extent(self, renderer=None):
        return self.get_path().get_extents(self.get_transform())
