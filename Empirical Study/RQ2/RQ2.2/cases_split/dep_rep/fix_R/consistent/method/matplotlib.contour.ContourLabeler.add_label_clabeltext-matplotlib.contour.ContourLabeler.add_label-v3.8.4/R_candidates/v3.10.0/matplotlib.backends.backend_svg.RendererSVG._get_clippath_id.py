    def _get_clippath_id(self, clippath):
        """
        Returns a stable and unique identifier for the *clippath* argument
        object within the current rendering context.

        This allows plots that include custom clip paths to produce identical
        SVG output on each render, provided that the :rc:`svg.hashsalt` config
        setting and the ``SOURCE_DATE_EPOCH`` build-time environment variable
        are set to fixed values.
        """
        if clippath not in self._clip_path_ids:
            self._clip_path_ids[clippath] = len(self._clip_path_ids)
        return self._clip_path_ids[clippath]
