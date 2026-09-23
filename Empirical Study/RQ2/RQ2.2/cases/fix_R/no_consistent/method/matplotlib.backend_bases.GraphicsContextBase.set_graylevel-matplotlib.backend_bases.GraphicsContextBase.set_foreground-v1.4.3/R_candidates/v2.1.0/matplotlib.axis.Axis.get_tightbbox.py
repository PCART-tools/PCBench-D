    def get_tightbbox(self, renderer):
        """
        Return a bounding box that encloses the axis. It only accounts
        tick labels, axis label, and offsetText.
        """
        if not self.get_visible():
            return

        ticks_to_draw = self._update_ticks(renderer)
        ticklabelBoxes, ticklabelBoxes2 = self._get_tick_bboxes(ticks_to_draw,
                                                                renderer)

        self._update_label_position(ticklabelBoxes, ticklabelBoxes2)

        self._update_offset_text_position(ticklabelBoxes, ticklabelBoxes2)
        self.offsetText.set_text(self.major.formatter.get_offset())

        bb = []

        for a in [self.label, self.offsetText]:
            if a.get_visible():
                bb.append(a.get_window_extent(renderer))

        bb.extend(ticklabelBoxes)
        bb.extend(ticklabelBoxes2)

        bb = [b for b in bb if b.width != 0 or b.height != 0]
        if bb:
            _bbox = mtransforms.Bbox.union(bb)
            return _bbox
        else:
            return None
