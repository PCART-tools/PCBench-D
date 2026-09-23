    def _set_title_offset_trans(self, title_offset_points):
        """
        Set the offset for the title either from :rc:`axes.titlepad`
        or from set_title kwarg ``pad``.
        """
        self.titleOffsetTrans = mtransforms.ScaledTranslation(
                0.0, title_offset_points / 72,
                self.figure.dpi_scale_trans)
        for _title in (self.title, self._left_title, self._right_title):
            _title.set_transform(self.transAxes + self.titleOffsetTrans)
            _title.set_clip_box(None)
