    def set_clip_box(self, clipbox):
        """
        Set the artist's clip `~.transforms.Bbox`.

        Parameters
        ----------
        clipbox : `matplotlib.transforms.Bbox`
        """
        super().set_clip_box(clipbox)
        self._update_clip_properties()
