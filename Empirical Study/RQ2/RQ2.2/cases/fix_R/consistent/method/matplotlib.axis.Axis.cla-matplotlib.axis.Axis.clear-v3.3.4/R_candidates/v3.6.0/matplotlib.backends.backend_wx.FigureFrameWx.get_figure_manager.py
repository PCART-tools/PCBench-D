    @_api.deprecated("3.6", alternative="frame.canvas.manager")
    def get_figure_manager(self):
        _log.debug("%s - get_figure_manager()", type(self))
        return self.canvas.manager
