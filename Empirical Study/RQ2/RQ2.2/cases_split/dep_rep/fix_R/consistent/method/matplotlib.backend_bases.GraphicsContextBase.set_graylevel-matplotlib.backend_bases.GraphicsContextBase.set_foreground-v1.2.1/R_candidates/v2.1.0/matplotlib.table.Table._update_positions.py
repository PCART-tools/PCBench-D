    def _update_positions(self, renderer):
        # called from renderer to allow more precise estimates of
        # widths and heights with get_window_extent

        # Do any auto width setting
        for col in self._autoColumns:
            self._auto_set_column_width(col, renderer)

        if self._autoFontsize:
            self._auto_set_font_size(renderer)

        # Align all the cells
        self._do_cell_alignment()

        bbox = self._get_grid_bbox(renderer)
        l, b, w, h = bbox.bounds

        if self._bbox is not None:
            # Position according to bbox
            rl, rb, rw, rh = self._bbox
            self.scale(rw / w, rh / h)
            ox = rl - l
            oy = rb - b
            self._do_cell_alignment()
        else:
            # Position using loc
            (BEST, UR, UL, LL, LR, CL, CR, LC, UC, C,
             TR, TL, BL, BR, R, L, T, B) = xrange(len(self.codes))
            # defaults for center
            ox = (0.5 - w / 2) - l
            oy = (0.5 - h / 2) - b
            if self._loc in (UL, LL, CL):   # left
                ox = self.AXESPAD - l
            if self._loc in (BEST, UR, LR, R, CR):  # right
                ox = 1 - (l + w + self.AXESPAD)
            if self._loc in (BEST, UR, UL, UC):     # upper
                oy = 1 - (b + h + self.AXESPAD)
            if self._loc in (LL, LR, LC):           # lower
                oy = self.AXESPAD - b
            if self._loc in (LC, UC, C):            # center x
                ox = (0.5 - w / 2) - l
            if self._loc in (CL, CR, C):            # center y
                oy = (0.5 - h / 2) - b

            if self._loc in (TL, BL, L):            # out left
                ox = - (l + w)
            if self._loc in (TR, BR, R):            # out right
                ox = 1.0 - l
            if self._loc in (TR, TL, T):            # out top
                oy = 1.0 - b
            if self._loc in (BL, BR, B):           # out bottom
                oy = - (b + h)

        self._offset(ox, oy)
