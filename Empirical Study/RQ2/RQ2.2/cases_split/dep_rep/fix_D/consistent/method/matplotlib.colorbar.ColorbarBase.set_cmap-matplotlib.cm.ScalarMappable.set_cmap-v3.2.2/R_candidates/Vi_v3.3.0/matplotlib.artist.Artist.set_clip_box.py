    def set_clip_box(self, clipbox):
        """
        Set the artist's clip `.Bbox`.

        Parameters
        ----------
        clipbox : `.Bbox`
        """
        self.clipbox = clipbox
        self.pchanged()
        self.stale = True
