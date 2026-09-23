class LineCollection(Collection):
    r"""
    Represents a sequence of `.Line2D`\s that should be drawn together.

    This class extends `.Collection` to represent a sequence of
    `.Line2D`\s instead of just a sequence of `.Patch`\s.
    Just as in `.Collection`, each property of a *LineCollection* may be either
    a single value or a list of values. This list is then used cyclically for
    each element of the LineCollection, so the property of the ``i``\th element
    of the collection is::

      prop[i % len(prop)]

    The properties of each member of a *LineCollection* default to their values
    in :rc:`lines.*` instead of :rc:`patch.*`, and the property *colors* is
    added in place of *edgecolors*.
    """

    _edge_default = True

    def __init__(self, segments,  # Can be None.
                 *,
                 zorder=2,        # Collection.zorder is 1
                 **kwargs
                 ):
        """
        Parameters
        ----------
        segments : list of array-like
            A sequence of (*line0*, *line1*, *line2*), where::

                linen = (x0, y0), (x1, y1), ... (xm, ym)

            or the equivalent numpy array with two columns. Each line
            can have a different number of segments.
        linewidths : float or list of float, default: :rc:`lines.linewidth`
            The width of each line in points.
        colors : color or list of color, default: :rc:`lines.color`
            A sequence of RGBA tuples (e.g., arbitrary color strings, etc, not
            allowed).
        antialiaseds : bool or list of bool, default: :rc:`lines.antialiased`
            Whether to use antialiasing for each line.
        zorder : int, default: 2
            zorder of the lines once drawn.

        facecolors : color or list of color, default: 'none'
            When setting *facecolors*, each line is interpreted as a boundary
            for an area, implicitly closing the path from the last point to the
            first point. The enclosed area is filled with *facecolor*.
            In order to manually specify what should count as the "interior" of
            each line, please use `.PathCollection` instead, where the
            "interior" can be specified by appropriate usage of
            `~.path.Path.CLOSEPOLY`.

        **kwargs
            Forwarded to `.Collection`.
        """
        # Unfortunately, mplot3d needs this explicit setting of 'facecolors'.
        kwargs.setdefault('facecolors', 'none')
        super().__init__(
            zorder=zorder,
            **kwargs)
        self.set_segments(segments)

    def set_segments(self, segments):
        if segments is None:
            return

        self._paths = [mpath.Path(seg) if isinstance(seg, np.ma.MaskedArray)
                       else mpath.Path(np.asarray(seg, float))
                       for seg in segments]
        self.stale = True

    set_verts = set_segments  # for compatibility with PolyCollection
    set_paths = set_segments

    def get_segments(self):
        """
        Returns
        -------
        list
            List of segments in the LineCollection. Each list item contains an
            array of vertices.
        """
        segments = []

        for path in self._paths:
            vertices = [
                vertex
                for vertex, _
                # Never simplify here, we want to get the data-space values
                # back and there in no way to know the "right" simplification
                # threshold so never try.
                in path.iter_segments(simplify=False)
            ]
            vertices = np.asarray(vertices)
            segments.append(vertices)

        return segments

    def _get_default_linewidth(self):
        return mpl.rcParams['lines.linewidth']

    def _get_default_antialiased(self):
        return mpl.rcParams['lines.antialiased']

    def _get_default_edgecolor(self):
        return mpl.rcParams['lines.color']

    def _get_default_facecolor(self):
        return 'none'

    def set_color(self, c):
        """
        Set the edgecolor(s) of the LineCollection.

        Parameters
        ----------
        c : color or list of colors
            Single color (all lines have same color), or a
            sequence of rgba tuples; if it is a sequence the lines will
            cycle through the sequence.
        """
        self.set_edgecolor(c)

    set_colors = set_color

    def get_color(self):
        return self._edgecolors

    get_colors = get_color  # for compatibility with old versions
