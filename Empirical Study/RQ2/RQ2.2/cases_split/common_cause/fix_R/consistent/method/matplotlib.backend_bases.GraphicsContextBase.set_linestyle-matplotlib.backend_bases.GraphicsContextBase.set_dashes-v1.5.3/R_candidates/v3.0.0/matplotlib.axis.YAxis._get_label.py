    def _get_label(self):
        # x in display coords (updated by _update_label_position)
        # y in axes coords
        label = mtext.Text(x=0, y=0.5,
                           # todo: get the label position
                           fontproperties=font_manager.FontProperties(
                               size=rcParams['axes.labelsize'],
                               weight=rcParams['axes.labelweight']),
                           color=rcParams['axes.labelcolor'],
                           verticalalignment='bottom',
                           horizontalalignment='center',
                           rotation='vertical',
                           rotation_mode='anchor')
        label.set_transform(mtransforms.blended_transform_factory(
            mtransforms.IdentityTransform(), self.axes.transAxes))

        self._set_artist_props(label)
        self.label_position = 'left'
        return label
