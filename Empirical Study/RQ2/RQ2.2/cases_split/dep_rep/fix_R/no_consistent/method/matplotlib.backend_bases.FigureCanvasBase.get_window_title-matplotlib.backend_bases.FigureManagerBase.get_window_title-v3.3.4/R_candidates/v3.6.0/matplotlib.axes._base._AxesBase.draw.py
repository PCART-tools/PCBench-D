    @martist.allow_rasterization
    def draw(self, renderer):
        # docstring inherited
        if renderer is None:
            raise RuntimeError('No renderer defined')
        if not self.get_visible():
            return
        self._unstale_viewLim()

        renderer.open_group('axes', gid=self.get_gid())

        # prevent triggering call backs during the draw process
        self._stale = True

        # loop over self and child Axes...
        locator = self.get_axes_locator()
        self.apply_aspect(locator(self, renderer) if locator else None)

        artists = self.get_children()
        artists.remove(self.patch)

        # the frame draws the edges around the Axes patch -- we
        # decouple these so the patch can be in the background and the
        # frame in the foreground. Do this before drawing the axis
        # objects so that the spine has the opportunity to update them.
        if not (self.axison and self._frameon):
            for spine in self.spines.values():
                artists.remove(spine)

        self._update_title_position(renderer)

        if not self.axison:
            for _axis in self._axis_map.values():
                artists.remove(_axis)

        if not self.figure.canvas.is_saving():
            artists = [
                a for a in artists
                if not a.get_animated() or isinstance(a, mimage.AxesImage)]
        artists = sorted(artists, key=attrgetter('zorder'))

        # rasterize artists with negative zorder
        # if the minimum zorder is negative, start rasterization
        rasterization_zorder = self._rasterization_zorder

        if (rasterization_zorder is not None and
                artists and artists[0].zorder < rasterization_zorder):
            renderer.start_rasterizing()
            artists_rasterized = [a for a in artists
                                  if a.zorder < rasterization_zorder]
            artists = [a for a in artists
                       if a.zorder >= rasterization_zorder]
        else:
            artists_rasterized = []

        # the patch draws the background rectangle -- the frame below
        # will draw the edges
        if self.axison and self._frameon:
            self.patch.draw(renderer)

        if artists_rasterized:
            for a in artists_rasterized:
                a.draw(renderer)
            renderer.stop_rasterizing()

        mimage._draw_list_compositing_images(
            renderer, self, artists, self.figure.suppressComposite)

        renderer.close_group('axes')
        self.stale = False
