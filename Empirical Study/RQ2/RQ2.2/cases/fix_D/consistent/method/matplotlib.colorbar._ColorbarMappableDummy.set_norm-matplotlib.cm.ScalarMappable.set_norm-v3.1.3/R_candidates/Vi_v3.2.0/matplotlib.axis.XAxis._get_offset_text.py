    def _get_offset_text(self):
        # x in axes coords, y in display coords (to be updated at draw time)
        offsetText = mtext.Text(x=1, y=0,
                                fontproperties=font_manager.FontProperties(
                                    size=rcParams['xtick.labelsize']),
                                color=rcParams['xtick.color'],
                                verticalalignment='top',
                                horizontalalignment='right')
        offsetText.set_transform(mtransforms.blended_transform_factory(
            self.axes.transAxes, mtransforms.IdentityTransform())
        )
        self._set_artist_props(offsetText)
        self.offset_text_position = 'bottom'
        return offsetText
