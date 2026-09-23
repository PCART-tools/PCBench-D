    def set_clip_path(self, path, transform=None):
        # docstring inherited
        super().set_clip_path(path, transform)
        self.gridline.set_clip_path(path, transform)
        self.stale = True
