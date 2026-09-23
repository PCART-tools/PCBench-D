    def get_tightbbox(self, renderer, bbox_extra_artists=None):
        """
        Return a (tight) bounding box of the figure in inches.

        Artists that have ``artist.set_in_layout(False)`` are not included
        in the bbox.

        Parameters
        ----------
        renderer : `.RendererBase` subclass
            renderer that will be used to draw the figures (i.e.
            ``fig.canvas.get_renderer()``)

        bbox_extra_artists : list of `.Artist` or ``None``
            List of artists to include in the tight bounding box.  If
            ``None`` (default), then all artist children of each Axes are
            included in the tight bounding box.

        Returns
        -------
        `.BboxBase`
            containing the bounding box (in figure inches).
        """

        bb = []
        if bbox_extra_artists is None:
            artists = self.get_default_bbox_extra_artists()
        else:
            artists = bbox_extra_artists

        for a in artists:
            bbox = a.get_tightbbox(renderer)
            if bbox is not None and (bbox.width != 0 or bbox.height != 0):
                bb.append(bbox)

        for ax in self.axes:
            if ax.get_visible():
                # some axes don't take the bbox_extra_artists kwarg so we
                # need this conditional....
                try:
                    bbox = ax.get_tightbbox(
                        renderer, bbox_extra_artists=bbox_extra_artists)
                except TypeError:
                    bbox = ax.get_tightbbox(renderer)
                bb.append(bbox)
        bb = [b for b in bb
              if (np.isfinite(b.width) and np.isfinite(b.height)
                  and (b.width != 0 or b.height != 0))]

        if len(bb) == 0:
            if hasattr(self, 'bbox_inches'):
                return self.bbox_inches
            else:
                # subfigures do not have bbox_inches, but do have a bbox
                bb = [self.bbox]

        _bbox = Bbox.union(bb)

        bbox_inches = TransformedBbox(_bbox, Affine2D().scale(1 / self.dpi))

        return bbox_inches
