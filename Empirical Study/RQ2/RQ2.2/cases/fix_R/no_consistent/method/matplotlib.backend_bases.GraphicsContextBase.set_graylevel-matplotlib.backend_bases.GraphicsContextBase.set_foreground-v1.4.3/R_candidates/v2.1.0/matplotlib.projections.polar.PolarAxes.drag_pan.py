    def drag_pan(self, button, key, x, y):
        p = self._pan_start

        if p.mode == 'drag_r_labels':
            startt, startr = p.trans_inverse.transform_point((p.x, p.y))
            t, r = p.trans_inverse.transform_point((x, y))

            # Deal with theta
            dt0 = t - startt
            dt1 = startt - t
            if abs(dt1) < abs(dt0):
                dt = abs(dt1) * np.sign(dt0) * -1.0
            else:
                dt = dt0 * -1.0
            dt = (dt / np.pi) * 180.0
            self.set_rlabel_position(p.r_label_angle - dt)

            trans, vert1, horiz1 = self.get_yaxis_text1_transform(0.0)
            trans, vert2, horiz2 = self.get_yaxis_text2_transform(0.0)
            for t in self.yaxis.majorTicks + self.yaxis.minorTicks:
                t.label1.set_va(vert1)
                t.label1.set_ha(horiz1)
                t.label2.set_va(vert2)
                t.label2.set_ha(horiz2)

        elif p.mode == 'zoom':
            startt, startr = p.trans_inverse.transform_point((p.x, p.y))
            t, r = p.trans_inverse.transform_point((x, y))

            # Deal with r
            scale = r / startr
            self.set_rmax(p.rmax / scale)
