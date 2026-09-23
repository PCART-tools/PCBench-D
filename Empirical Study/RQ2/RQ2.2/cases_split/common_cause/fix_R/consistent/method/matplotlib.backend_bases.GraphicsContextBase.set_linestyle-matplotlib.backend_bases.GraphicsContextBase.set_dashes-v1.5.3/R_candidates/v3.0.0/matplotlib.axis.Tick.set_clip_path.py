    def set_clip_path(self, clippath, transform=None):
        artist.Artist.set_clip_path(self, clippath, transform)
        self.gridline.set_clip_path(clippath, transform)
        self.stale = True
