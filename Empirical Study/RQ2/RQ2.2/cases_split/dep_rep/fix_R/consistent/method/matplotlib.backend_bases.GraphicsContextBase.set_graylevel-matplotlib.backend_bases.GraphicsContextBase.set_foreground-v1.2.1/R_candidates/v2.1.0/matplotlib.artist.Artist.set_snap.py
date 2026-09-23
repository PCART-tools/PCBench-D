    def set_snap(self, snap):
        """
        Sets the snap setting which may be:

          * True: snap vertices to the nearest pixel center

          * False: leave vertices as-is

          * None: (auto) If the path contains only rectilinear line
            segments, round to the nearest pixel center

        Only supported by the Agg and MacOSX backends.
        """
        self._snap = snap
        self.stale = True
