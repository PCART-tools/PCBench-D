    def show(self):
        if not self._shown:
            self.display_js()
            self._create_comm()
        else:
            self.canvas.draw_idle()
        self._shown = True
        # plt.figure adds an event which makes the figure in focus the active
        # one. Disable this behaviour, as it results in figures being put as
        # the active figure after they have been shown, even in non-interactive
        # mode.
        if hasattr(self, '_cidgcf'):
            self.canvas.mpl_disconnect(self._cidgcf)
        if not is_interactive():
            from matplotlib._pylab_helpers import Gcf
            Gcf.figs.pop(self.num, None)
