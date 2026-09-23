    def _fully_clipped_to_axes(self):
        """
        Return a boolean flag, ``True`` if the artist is clipped to the Axes
        and can thus be skipped in layout calculations. Requires `get_clip_on`
        is True, one of `clip_box` or `clip_path` is set, ``clip_box.extents``
        is equivalent to ``ax.bbox.extents`` (if set), and ``clip_path._patch``
        is equivalent to ``ax.patch`` (if set).
        """
        # Note that ``clip_path.get_fully_transformed_path().get_extents()``
        # cannot be directly compared to ``axes.bbox.extents`` because the
        # extents may be undefined (i.e. equivalent to ``Bbox.null()``)
        # before the associated artist is drawn, and this method is meant
        # to determine whether ``axes.get_tightbbox()`` may bypass drawing
        clip_box = self.get_clip_box()
        clip_path = self.get_clip_path()
        return (self.axes is not None
                and self.get_clip_on()
                and (clip_box is not None or clip_path is not None)
                and (clip_box is None
                     or np.all(clip_box.extents == self.axes.bbox.extents))
                and (clip_path is None
                     or isinstance(clip_path, TransformedPatchPath)
                     and clip_path._patch is self.axes.patch))
