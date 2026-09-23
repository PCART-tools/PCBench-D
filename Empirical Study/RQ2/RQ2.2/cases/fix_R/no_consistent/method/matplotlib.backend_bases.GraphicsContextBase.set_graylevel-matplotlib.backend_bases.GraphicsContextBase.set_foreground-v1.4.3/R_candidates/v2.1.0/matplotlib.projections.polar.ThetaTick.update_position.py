    def update_position(self, loc):
        super(ThetaTick, self).update_position(loc)
        axes = self.axes
        angle = (loc * axes.get_theta_direction() +
                 axes.get_theta_offset() - np.pi / 2)

        if self.tick1On:
            marker = self.tick1line.get_marker()
            if marker in (mmarkers.TICKUP, '|'):
                trans = mtransforms.Affine2D().scale(1.0, 1.0).rotate(angle)
            elif marker == mmarkers.TICKDOWN:
                trans = mtransforms.Affine2D().scale(1.0, -1.0).rotate(angle)
            else:
                # Don't modify custom tick line markers.
                trans = self.tick1line._marker._transform
            self.tick1line._marker._transform = trans
        if self.tick2On:
            marker = self.tick2line.get_marker()
            if marker in (mmarkers.TICKUP, '|'):
                trans = mtransforms.Affine2D().scale(1.0, 1.0).rotate(angle)
            elif marker == mmarkers.TICKDOWN:
                trans = mtransforms.Affine2D().scale(1.0, -1.0).rotate(angle)
            else:
                # Don't modify custom tick line markers.
                trans = self.tick2line._marker._transform
            self.tick2line._marker._transform = trans

        mode, user_angle = self._labelrotation
        if mode == 'default':
            angle = 0
        else:
            if angle > np.pi / 2:
                angle -= np.pi
            elif angle < -np.pi / 2:
                angle += np.pi
        angle = np.rad2deg(angle) + user_angle
        if self.label1On:
            self.label1.set_rotation(angle)
        if self.label2On:
            self.label2.set_rotation(angle)

        # This extra padding helps preserve the look from previous releases but
        # is also needed because labels are anchored to their center.
        pad = self._pad + 7
        self._update_padding(pad,
                             self._loc * axes.get_theta_direction() +
                             axes.get_theta_offset())
