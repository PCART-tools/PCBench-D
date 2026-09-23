    def set_clip_path(self, clippath, transform=None):
        martist.Artist.set_clip_path(self, clippath, transform)
        for child in self.majorTicks + self.minorTicks:
            child.set_clip_path(clippath, transform)
        self.stale = True
