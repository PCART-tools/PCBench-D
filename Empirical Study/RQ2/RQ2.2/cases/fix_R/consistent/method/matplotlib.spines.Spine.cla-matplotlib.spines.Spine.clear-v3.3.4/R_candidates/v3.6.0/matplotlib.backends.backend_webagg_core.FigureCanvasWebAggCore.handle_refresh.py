    def handle_refresh(self, event):
        figure_label = self.figure.get_label()
        if not figure_label:
            figure_label = "Figure {0}".format(self.manager.num)
        self.send_event('figure_label', label=figure_label)
        self._force_full = True
        if self.toolbar:
            # Normal toolbar init would refresh this, but it happens before the
            # browser canvas is set up.
            self.toolbar.set_history_buttons()
        self.draw_idle()
