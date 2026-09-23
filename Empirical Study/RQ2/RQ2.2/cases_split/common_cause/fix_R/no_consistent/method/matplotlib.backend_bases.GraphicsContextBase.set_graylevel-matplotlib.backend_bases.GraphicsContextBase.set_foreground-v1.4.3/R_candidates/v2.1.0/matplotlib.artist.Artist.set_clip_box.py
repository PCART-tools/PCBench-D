    def set_clip_box(self, clipbox):
        """
        Set the artist's clip :class:`~matplotlib.transforms.Bbox`.

        ACCEPTS: a :class:`matplotlib.transforms.Bbox` instance
        """
        self.clipbox = clipbox
        self.pchanged()
        self.stale = True
