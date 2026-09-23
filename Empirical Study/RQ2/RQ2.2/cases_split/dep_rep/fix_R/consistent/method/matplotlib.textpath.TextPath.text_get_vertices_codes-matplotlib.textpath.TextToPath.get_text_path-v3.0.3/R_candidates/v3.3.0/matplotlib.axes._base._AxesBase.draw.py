    @martist.allow_rasterization
    @cbook._delete_parameter(
        "3.3", "inframe", alternative="Axes.redraw_in_frame()")
    def draw(self, renderer=None, inframe=False):
        # docstring inherited
        if renderer is None:
            cbook.warn_deprecated(
                "3.3", message="Support for not passing the 'renderer' "
                "parameter to Axes.draw() is deprecated since %(since)s and "
                "will be removed %(removal)s.  Use axes.draw_artist(axes) "
                "instead.")
            renderer = self.figure._cachedRenderer
        if renderer is None:
            raise RuntimeError('No renderer defined')
        if not self.get_visible():
            return
        self._unstale_viewLim()

        renderer.open_group('axes', gid=self.get_gid())

        # prevent triggering call backs during the draw process
        self._stale = True

        # loop over self and child axes...
        locator = self.get_axes_locator()
        if locator:
            pos = locator(self, renderer)
            self.apply_aspect(pos)
        else:
            self.apply_aspect()

        artists = self.get_children()
        artists.remove(self.patch)

        # the frame draws the edges around the axes patch -- we
        # decouple these so the patch can be in the background and the
        # frame in the foreground. Do this before drawing the axis
        # objects so that the spine has the opportunity to update them.
        if not (self.axison and self._frameon):
            for spine in self.spines.values():
                artists.remove(spine)

        self._update_title_position(renderer)

        if not self.axison or inframe:
            for _axis in self._get_axis_list():
                artists.remove(_axis)

        if inframe:
            artists.remove(self.title)
            artists.remove(self._left_title)
            artists.remove(self._right_title)

        if not self.figure.canvas.is_saving():
            artists = [a for a in artists
                       if not a.get_animated() or a in self.images]
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

        mimage._draw_list_compositing_images(renderer, self, artists)

        renderer.close_group('axes')
        self.stale = False
