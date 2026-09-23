    def set_clip_box(self, clipbox):
        """
        Set the artist's clip :class:`~matplotlib.transforms.Bbox`.

        ACCEPTS: a :class:`matplotlib.transforms.Bbox` instance
        """
        super(Text, self).set_clip_box(clipbox)
        self._update_clip_properties()
