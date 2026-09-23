    def set_clip_path(self, clippath, transform=None):
        # docstring inherited
        super().set_clip_path(clippath, transform)
        self.gridline.set_clip_path(clippath, transform)
        self.stale = True
