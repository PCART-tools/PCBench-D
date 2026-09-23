    def _get_window_indexer(self, window: int) -> BaseIndexer:
        """
        Return an indexer class that will compute the window start and end bounds
        """
        if isinstance(self.window, BaseIndexer):
            return self.window
        if self.is_freq_type:
            return VariableWindowIndexer(index_array=self._on.asi8, window_size=window)
        return FixedWindowIndexer(window_size=window)
