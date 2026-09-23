    def _get_window(self, other=None, win_type: Optional[str] = None) -> int:
        """
        Return window length.

        Parameters
        ----------
        other :
            ignored, exists for compatibility
        win_type :
            ignored, exists for compatibility

        Returns
        -------
        window : int
        """
        if isinstance(self.window, BaseIndexer):
            return self.min_periods or 0
        return self.window
