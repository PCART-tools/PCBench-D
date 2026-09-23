    def release_zoom(self, event):
        """Callback for mouse button release in zoom to rect mode."""
        if self._zoom_info is None:
            return

        # We don't check the event button here, so that zooms can be cancelled
        # by (pressing and) releasing another mouse button.
        self.canvas.mpl_disconnect(self._zoom_info["cid"])
        self.remove_rubberband()

        start_x, start_y = self._zoom_info["start_xy"]

        for i, ax in enumerate(self._zoom_info["axes"]):
            x, y = event.x, event.y
            # ignore singular clicks - 5 pixels is a threshold
            # allows the user to "cancel" a zoom action
            # by zooming by less than 5 pixels
            if ((abs(x - start_x) < 5 and event.key != "y") or
                    (abs(y - start_y) < 5 and event.key != "x")):
                self._xypress = None
                release = cbook._deprecate_method_override(
                    __class__.press, self, since="3.3", message="Calling an "
                    "overridden release() at zoom stop is deprecated since "
                    "%(since)s and will be removed %(removal)s; override "
                    "release_zoom() instead.")
                if release is not None:
                    release(event)
                self._draw()
                return

            # Detect whether this axes is twinned with an earlier axes in the
            # list of zoomed axes, to avoid double zooming.
            twinx = any(ax.get_shared_x_axes().joined(ax, prev)
                        for prev in self._zoom_info["axes"][:i])
            twiny = any(ax.get_shared_y_axes().joined(ax, prev)
                        for prev in self._zoom_info["axes"][:i])

            ax._set_view_from_bbox(
                (start_x, start_y, x, y), self._zoom_info["direction"],
                event.key, twinx, twiny)

        self._draw()
        self._zoom_info = None

        self.push_current()
        release = cbook._deprecate_method_override(
            __class__.release, self, since="3.3", message="Calling an "
            "overridden release() at zoom stop is deprecated since %(since)s "
            "and will be removed %(removal)s; override release_zoom() "
            "instead.")
        if release is not None:
            release(event)
