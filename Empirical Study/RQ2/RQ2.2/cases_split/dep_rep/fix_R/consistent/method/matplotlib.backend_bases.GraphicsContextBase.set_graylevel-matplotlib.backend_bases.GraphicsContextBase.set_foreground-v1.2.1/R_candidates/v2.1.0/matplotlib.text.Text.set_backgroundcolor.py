    def set_backgroundcolor(self, color):
        """
        Set the background color of the text by updating the bbox.

        .. seealso::

            :meth:`set_bbox`
               To change the position of the bounding box.

        ACCEPTS: any matplotlib color
        """
        if self._bbox_patch is None:
            self.set_bbox(dict(facecolor=color, edgecolor=color))
        else:
            self._bbox_patch.update(dict(facecolor=color))

        self._update_clip_properties()
        self.stale = True
