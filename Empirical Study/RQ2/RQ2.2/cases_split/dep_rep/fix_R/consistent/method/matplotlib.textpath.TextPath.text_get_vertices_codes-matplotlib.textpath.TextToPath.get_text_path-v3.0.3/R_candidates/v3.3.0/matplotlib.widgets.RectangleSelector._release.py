    def _release(self, event):
        """on button release event"""
        if not self.interactive:
            self.to_draw.set_visible(False)

        # update the eventpress and eventrelease with the resulting extents
        x1, x2, y1, y2 = self.extents
        self.eventpress.xdata = x1
        self.eventpress.ydata = y1
        xy1 = self.ax.transData.transform([x1, y1])
        self.eventpress.x, self.eventpress.y = xy1

        self.eventrelease.xdata = x2
        self.eventrelease.ydata = y2
        xy2 = self.ax.transData.transform([x2, y2])
        self.eventrelease.x, self.eventrelease.y = xy2

        # calculate dimensions of box or line
        if self.spancoords == 'data':
            spanx = abs(self.eventpress.xdata - self.eventrelease.xdata)
            spany = abs(self.eventpress.ydata - self.eventrelease.ydata)
        elif self.spancoords == 'pixels':
            spanx = abs(self.eventpress.x - self.eventrelease.x)
            spany = abs(self.eventpress.y - self.eventrelease.y)
        else:
            cbook._check_in_list(['data', 'pixels'],
                                 spancoords=self.spancoords)
        # check if drawn distance (if it exists) is not too small in
        # either x or y-direction
        if (self.drawtype != 'none'
                and (self.minspanx is not None and spanx < self.minspanx
                     or self.minspany is not None and spany < self.minspany)):
            for artist in self.artists:
                artist.set_visible(False)
            self.update()
            return

        # call desired function
        self.onselect(self.eventpress, self.eventrelease)
        self.update()

        return False
