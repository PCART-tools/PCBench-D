    def get_legend_handler_map(self):
        """
        return the handler map.
        """

        default_handler_map = self.get_default_handler_map()

        if self._custom_handler_map:
            hm = default_handler_map.copy()
            hm.update(self._custom_handler_map)
            return hm
        else:
            return default_handler_map
