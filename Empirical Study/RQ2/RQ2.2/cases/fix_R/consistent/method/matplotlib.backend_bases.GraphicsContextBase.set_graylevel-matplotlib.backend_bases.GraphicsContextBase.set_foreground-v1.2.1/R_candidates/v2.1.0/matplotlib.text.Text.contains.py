    def contains(self, mouseevent):
        """Test whether the mouse event occurred in the patch.

        In the case of text, a hit is true anywhere in the
        axis-aligned bounding-box containing the text.

        Returns True or False.
        """
        if callable(self._contains):
            return self._contains(self, mouseevent)

        if not self.get_visible() or self._renderer is None:
            return False, {}

        l, b, w, h = self.get_window_extent().bounds
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
