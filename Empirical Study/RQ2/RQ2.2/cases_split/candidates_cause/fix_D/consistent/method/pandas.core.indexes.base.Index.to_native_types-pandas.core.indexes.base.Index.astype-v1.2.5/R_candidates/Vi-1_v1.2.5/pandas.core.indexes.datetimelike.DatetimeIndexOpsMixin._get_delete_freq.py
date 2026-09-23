    def _get_delete_freq(self, loc: int):
        """
        Find the `freq` for self.delete(loc).
        """
        freq = None
        if is_period_dtype(self.dtype):
            freq = self.freq
        elif self.freq is not None:
            if is_integer(loc):
                if loc in (0, -len(self), -1, len(self) - 1):
                    freq = self.freq
            else:
                if is_list_like(loc):
                    loc = lib.maybe_indices_to_slice(
                        np.asarray(loc, dtype=np.intp), len(self)
                    )
                if isinstance(loc, slice) and loc.step in (1, None):
                    if loc.start in (0, None) or loc.stop in (len(self), None):
                        freq = self.freq
        return freq
