    def findfont(self, prop, fontext='ttf', directory=None,
                 fallback_to_default=True, rebuild_if_missing=True):
        """
        Search the font list for the font that most closely matches
        the :class:`FontProperties` *prop*.

        :meth:`findfont` performs a nearest neighbor search.  Each
        font is given a similarity score to the target font
        properties.  The first font with the highest score is
        returned.  If no matches below a certain threshold are found,
        the default font (usually DejaVu Sans) is returned.

        `directory`, is specified, will only return fonts from the
        given directory (or subdirectory of that directory).

        The result is cached, so subsequent lookups don't have to
        perform the O(n) nearest neighbor search.

        If `fallback_to_default` is True, will fallback to the default
        font family (usually "DejaVu Sans" or "Helvetica") if
        the first lookup hard-fails.

        See the `W3C Cascading Style Sheet, Level 1
        <http://www.w3.org/TR/1998/REC-CSS2-19980512/>`_ documentation
        for a description of the font finding algorithm.
        """
        # Pass the relevant rcParams (and the font manager, as `self`) to
        # _findfont_cached so to prevent using a stale cache entry after an
        # rcParam was changed.
        rc_params = tuple(tuple(rcParams[key]) for key in [
            "font.serif", "font.sans-serif", "font.cursive", "font.fantasy",
            "font.monospace"])
        return self._findfont_cached(
            prop, fontext, directory, fallback_to_default, rebuild_if_missing,
            rc_params)
