    @martist.allow_rasterization
    def draw(self, renderer, *args, **kwargs):
        'Draw the axis lines, grid lines, tick lines and labels'

        if not self.get_visible():
            return
        renderer.open_group(__name__)

        ticks_to_draw = self._update_ticks()
        ticklabelBoxes, ticklabelBoxes2 = self._get_tick_bboxes(ticks_to_draw,
                                                                renderer)

        for tick in ticks_to_draw:
            tick.draw(renderer)

        # scale up the axis label box to also find the neighbors, not
        # just the tick labels that actually overlap note we need a
        # *copy* of the axis label box because we don't wan't to scale
        # the actual bbox

        self._update_label_position(renderer)

        self.label.draw(renderer)

        self._update_offset_text_position(ticklabelBoxes, ticklabelBoxes2)
        self.offsetText.set_text(self.major.formatter.get_offset())
        self.offsetText.draw(renderer)

        renderer.close_group(__name__)
        self.stale = False
