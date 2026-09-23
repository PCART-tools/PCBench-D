    def _update_viewlim(self):  # Inline after deprecation elapses.
        viewlim = self._parent_axes.viewLim.frozen()
        mode = self.get_viewlim_mode()
        if mode is None:
            pass
        elif mode == "equal":
            self.axes.viewLim.set(viewlim)
        elif mode == "transform":
            self.axes.viewLim.set(
                viewlim.transformed(self.transAux.inverted()))
        else:
            _api.check_in_list([None, "equal", "transform"], mode=mode)
