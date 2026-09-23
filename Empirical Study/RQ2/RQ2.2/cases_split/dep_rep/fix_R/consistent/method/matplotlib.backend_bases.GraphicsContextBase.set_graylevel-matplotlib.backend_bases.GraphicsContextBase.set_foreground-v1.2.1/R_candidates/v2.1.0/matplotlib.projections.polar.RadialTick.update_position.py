    def update_position(self, loc):
        super(RadialTick, self).update_position(loc)
        axes = self.axes
        thetamin = axes.get_thetamin()
        thetamax = axes.get_thetamax()
        direction = axes.get_theta_direction()
        offset_rad = axes.get_theta_offset()
        offset = np.rad2deg(offset_rad)
        full = _is_full_circle_deg(thetamin, thetamax)

        if full:
            angle = axes.get_rlabel_position() * direction + offset - 90
            tick_angle = 0
            if angle > 90:
                text_angle = angle - 180
            elif angle < -90:
                text_angle = angle + 180
            else:
                text_angle = angle
        else:
            angle = thetamin * direction + offset - 90
            if direction > 0:
                tick_angle = np.deg2rad(angle)
            else:
                tick_angle = np.deg2rad(angle + 180)
            if angle > 90:
                text_angle = angle - 180
            elif angle < -90:
                text_angle = angle + 180
            else:
                text_angle = angle
        mode, user_angle = self._labelrotation
        if mode == 'auto':
            text_angle += user_angle
        else:
            text_angle = user_angle
        if self.label1On:
            if full:
                ha = 'left'
                va = 'bottom'
            else:
                ha, va = self._determine_anchor(angle, True)
            self.label1.set_ha(ha)
            self.label1.set_va(va)
            self.label1.set_rotation(text_angle)
        if self.tick1On:
            marker = self.tick1line.get_marker()
            if marker == mmarkers.TICKLEFT:
                trans = (mtransforms.Affine2D()
                         .scale(1.0, 1.0)
                         .rotate(tick_angle))
            elif marker == '_':
                trans = (mtransforms.Affine2D()
                         .scale(1.0, 1.0)
                         .rotate(tick_angle + np.pi / 2))
            elif marker == mmarkers.TICKRIGHT:
                trans = (mtransforms.Affine2D()
                         .scale(-1.0, 1.0)
                         .rotate(tick_angle))
            else:
                # Don't modify custom tick line markers.
                trans = self.tick1line._marker._transform
            self.tick1line._marker._transform = trans

        if full:
            self.label2On = False
            self.tick2On = False
        else:
            angle = thetamax * direction + offset - 90
            if direction > 0:
                tick_angle = np.deg2rad(angle)
            else:
                tick_angle = np.deg2rad(angle + 180)
            if angle > 90:
                text_angle = angle - 180
            elif angle < -90:
                text_angle = angle + 180
            else:
                text_angle = angle
        mode, user_angle = self._labelrotation
        if mode == 'auto':
            text_angle += user_angle
        else:
            text_angle = user_angle
        if self.label2On:
            ha, va = self._determine_anchor(angle, False)
            self.label2.set_ha(ha)
            self.label2.set_va(va)
            self.label2.set_rotation(text_angle)
        if self.tick2On:
            marker = self.tick2line.get_marker()
            if marker == mmarkers.TICKLEFT:
                trans = (mtransforms.Affine2D()
                         .scale(1.0, 1.0)
                         .rotate(tick_angle))
            elif marker == '_':
                trans = (mtransforms.Affine2D()
                         .scale(1.0, 1.0)
                         .rotate(tick_angle + np.pi / 2))
            elif marker == mmarkers.TICKRIGHT:
                trans = (mtransforms.Affine2D()
                         .scale(-1.0, 1.0)
                         .rotate(tick_angle))
            else:
                # Don't modify custom tick line markers.
                trans = self.tick2line._marker._transform
            self.tick2line._marker._transform = trans
