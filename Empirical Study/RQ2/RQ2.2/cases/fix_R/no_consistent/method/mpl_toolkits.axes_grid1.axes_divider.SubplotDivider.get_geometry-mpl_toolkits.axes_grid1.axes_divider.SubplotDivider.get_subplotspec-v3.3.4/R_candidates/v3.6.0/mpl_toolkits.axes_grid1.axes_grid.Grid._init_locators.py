    def _init_locators(self):

        h = []
        h_ax_pos = []
        for _ in range(self._ncols):
            if h:
                h.append(self._horiz_pad_size)
            h_ax_pos.append(len(h))
            sz = Size.Scaled(1)
            h.append(sz)

        v = []
        v_ax_pos = []
        for _ in range(self._nrows):
            if v:
                v.append(self._vert_pad_size)
            v_ax_pos.append(len(v))
            sz = Size.Scaled(1)
            v.append(sz)

        for i in range(self.ngrids):
            col, row = self._get_col_row(i)
            locator = self._divider.new_locator(
                nx=h_ax_pos[col], ny=v_ax_pos[self._nrows - 1 - row])
            self.axes_all[i].set_axes_locator(locator)

        self._divider.set_horizontal(h)
        self._divider.set_vertical(v)
