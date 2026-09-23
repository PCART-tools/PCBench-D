    @martist.allow_rasterization
    def draw(self, renderer, *args, **kwargs):
        # docstring inherited

        if not self.get_visible():
            return
        renderer.open_group(__name__, gid=self.get_gid())

        ticks_to_draw = self._update_ticks()
        tlb1, tlb2 = self._get_ticklabel_bboxes(ticks_to_draw, renderer)

        for tick in ticks_to_draw:
            tick.draw(renderer)

        # Scale up the axis label box to also find the neighbors, not just the
        # tick labels that actually overlap.  We need a *copy* of the axis
        # label box because we don't want to scale the actual bbox.

        self._update_label_position(renderer)

        self.label.draw(renderer)

        self._update_offset_text_position(tlb1, tlb2)
        self.offsetText.set_text(self.major.formatter.get_offset())
        self.offsetText.draw(renderer)

        renderer.close_group(__name__)
        self.stale = False
