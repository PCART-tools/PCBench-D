    def _get_ticklabel_bboxes(self, ticks, renderer=None):
        """Return lists of bboxes for ticks' label1's and label2's."""
        if renderer is None:
            renderer = self.get_figure(root=True)._get_renderer()
        return ([tick.label1.get_window_extent(renderer)
                 for tick in ticks if tick.label1.get_visible()],
                [tick.label2.get_window_extent(renderer)
                 for tick in ticks if tick.label2.get_visible()])
