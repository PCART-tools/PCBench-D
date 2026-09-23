    def contains(self, mouseevent):
        """Test whether the mouse event occurred in the patch.

        In the case of text, a hit is true anywhere in the
        axis-aligned bounding-box containing the text.

        Returns
        -------
        bool : bool
        """
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info

        if not self.get_visible() or self._renderer is None:
            return False, {}

        # Explicitly use Text.get_window_extent(self) and not
        # self.get_window_extent() so that Annotation.contains does not
        # accidentally cover the entire annotation bounding box.
        l, b, w, h = Text.get_window_extent(self).bounds
        r, t = l + w, b + h

        x, y = mouseevent.x, mouseevent.y
        inside = (l <= x <= r and b <= y <= t)
        cattr = {}

        # if the text has a surrounding patch, also check containment for it,
        # and merge the results with the results for the text.
        if self._bbox_patch:
            patch_inside, patch_cattr = self._bbox_patch.contains(mouseevent)
            inside = inside or patch_inside
            cattr["bbox_patch"] = patch_cattr

        return inside, cattr
