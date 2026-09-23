    def get_tightbbox(self, renderer):
        """
        Return a bounding box that encloses the axis. It only accounts
        tick labels, axis label, and offsetText.
        """
        if not self.get_visible():
            return

        ticks_to_draw = self._update_ticks()

        self._update_label_position(renderer)

        # go back to just this axis's tick labels
        ticklabelBoxes, ticklabelBoxes2 = self._get_tick_bboxes(
                    ticks_to_draw, renderer)

        self._update_offset_text_position(ticklabelBoxes, ticklabelBoxes2)
        self.offsetText.set_text(self.major.formatter.get_offset())

        bboxes = [
            *(a.get_window_extent(renderer)
              for a in [self.label, self.offsetText]
              if a.get_visible()),
            *ticklabelBoxes,
            *ticklabelBoxes2,
        ]
        bboxes = [b for b in bboxes
                  if 0 < b.width < np.inf and 0 < b.height < np.inf]
        if bboxes:
            return mtransforms.Bbox.union(bboxes)
        else:
            return None
