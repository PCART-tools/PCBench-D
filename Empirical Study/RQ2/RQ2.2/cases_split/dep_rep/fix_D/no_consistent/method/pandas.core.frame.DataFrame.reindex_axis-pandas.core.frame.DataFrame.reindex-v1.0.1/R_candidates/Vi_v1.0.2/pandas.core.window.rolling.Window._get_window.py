    def _get_window(
        self, other=None, win_type: Optional[Union[str, Tuple]] = None
    ) -> np.ndarray:
        """
        Get the window, weights.

        Parameters
        ----------
        other :
            ignored, exists for compatibility
        win_type : str, or tuple
            type of window to create

        Returns
        -------
        window : ndarray
            the window, weights
        """

        window = self.window
        if isinstance(window, (list, tuple, np.ndarray)):
            return com.asarray_tuplesafe(window).astype(float)
        elif is_integer(window):
            import scipy.signal as sig

            # GH #15662. `False` makes symmetric window, rather than periodic.
            return sig.get_window(win_type, window, False).astype(float)
