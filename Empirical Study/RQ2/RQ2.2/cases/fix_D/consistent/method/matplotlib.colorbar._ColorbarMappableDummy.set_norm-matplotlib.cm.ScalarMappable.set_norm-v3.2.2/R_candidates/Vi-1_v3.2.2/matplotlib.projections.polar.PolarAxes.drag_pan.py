    def drag_pan(self, button, key, x, y):
        p = self._pan_start

        if p.mode == 'drag_r_labels':
            (startt, startr), (t, r) = p.trans_inverse.transform(
                [(p.x, p.y), (x, y)])

            # Deal with theta
            dt = np.rad2deg(startt - t)
            self.set_rlabel_position(p.r_label_angle - dt)

            trans, vert1, horiz1 = self.get_yaxis_text1_transform(0.0)
            trans, vert2, horiz2 = self.get_yaxis_text2_transform(0.0)
            for t in self.yaxis.majorTicks + self.yaxis.minorTicks:
                t.label1.set_va(vert1)
                t.label1.set_ha(horiz1)
                t.label2.set_va(vert2)
                t.label2.set_ha(horiz2)

        elif p.mode == 'zoom':
            (startt, startr), (t, r) = p.trans_inverse.transform(
                [(p.x, p.y), (x, y)])

            # Deal with r
            scale = r / startr
            self.set_rmax(p.rmax / scale)
