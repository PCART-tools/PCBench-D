    def _get_offset_text(self):
        # x in display coords, y in axes coords (to be updated at draw time)
        offsetText = mtext.Text(x=0, y=0.5,
                                fontproperties=font_manager.FontProperties(
                                    size=rcParams['ytick.labelsize']
                                ),
                                color=rcParams['ytick.color'],
                                verticalalignment='baseline',
                                horizontalalignment='left')
        offsetText.set_transform(mtransforms.blended_transform_factory(
            self.axes.transAxes, mtransforms.IdentityTransform())
        )
        self._set_artist_props(offsetText)
        self.offset_text_position = 'left'
        return offsetText
