    def _seek_check(self, frame):
        if (
            frame < self._min_frame
            # Only check upper limit on frames if additional seek operations
            # are not required to do so
            or (
                not (hasattr(self, "_n_frames") and self._n_frames is None)
                and frame >= self.n_frames + self._min_frame
            )
        ):
            msg = "attempt to seek outside sequence"
            raise EOFError(msg)

        return self.tell() != frame
