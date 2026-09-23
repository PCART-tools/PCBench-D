    def _get_label_clabeltext(self, x, y, rotation):
        # x, y, rotation is given in pixel coordinate. Convert them to
        # the data coordinate and create a label using ClabelText
        # class. This way, the rotation of the clabel is along the
        # contour line always.
        transDataInv = self.axes.transData.inverted()
        dx, dy = transDataInv.transform((x, y))
        drotation = transDataInv.transform_angles(np.array([rotation]),
                                                  np.array([[x, y]]))
        t = ClabelText(dx, dy, rotation=drotation[0],
                       horizontalalignment='center',
                       verticalalignment='center', zorder=self._clabel_zorder)

        return t
