    def get_default_bbox_extra_artists(self):
        """
        Return a default list of artists that are used for the bounding box
        calculation.

        Artists are excluded either by not being visible or
        ``artist.set_in_layout(False)``.
        """

        artists = self.get_children()

        for axis in self._axis_map.values():
            # axis tight bboxes are calculated separately inside
            # Axes.get_tightbbox() using for_layout_only=True
            artists.remove(axis)
        if not (self.axison and self._frameon):
            # don't do bbox on spines if frame not on.
            for spine in self.spines.values():
                artists.remove(spine)

        artists.remove(self.title)
        artists.remove(self._left_title)
        artists.remove(self._right_title)

        # always include types that do not internally implement clipping
        # to Axes. may have clip_on set to True and clip_box equivalent
        # to ax.bbox but then ignore these properties during draws.
        noclip = (_AxesBase, maxis.Axis,
                  offsetbox.AnnotationBbox, offsetbox.OffsetBox)
        return [a for a in artists if a.get_visible() and a.get_in_layout()
                and (isinstance(a, noclip) or not a._fully_clipped_to_axes())]
