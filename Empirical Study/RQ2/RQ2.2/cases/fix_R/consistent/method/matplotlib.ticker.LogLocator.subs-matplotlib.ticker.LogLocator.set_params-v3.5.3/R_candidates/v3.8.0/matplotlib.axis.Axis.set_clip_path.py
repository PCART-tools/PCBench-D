    @_api.rename_parameter("3.8", "clippath", "path")
    def set_clip_path(self, path, transform=None):
        super().set_clip_path(path, transform)
        for child in self.majorTicks + self.minorTicks:
            child.set_clip_path(path, transform)
        self.stale = True
