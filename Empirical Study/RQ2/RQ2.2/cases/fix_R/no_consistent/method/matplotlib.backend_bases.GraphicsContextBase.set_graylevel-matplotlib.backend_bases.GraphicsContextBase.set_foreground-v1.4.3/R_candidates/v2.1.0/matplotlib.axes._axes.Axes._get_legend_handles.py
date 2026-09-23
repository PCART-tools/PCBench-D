    def _get_legend_handles(self, legend_handler_map=None):
        """
        Return a generator of artists that can be used as handles in
        a legend.

        """
        handles_original = (self.lines + self.patches +
                            self.collections + self.containers)
        handler_map = mlegend.Legend.get_default_handler_map()

        if legend_handler_map is not None:
            handler_map = handler_map.copy()
            handler_map.update(legend_handler_map)

        has_handler = mlegend.Legend.get_legend_handler

        for handle in handles_original:
            label = handle.get_label()
            if label != '_nolegend_' and has_handler(handler_map, handle):
                yield handle
