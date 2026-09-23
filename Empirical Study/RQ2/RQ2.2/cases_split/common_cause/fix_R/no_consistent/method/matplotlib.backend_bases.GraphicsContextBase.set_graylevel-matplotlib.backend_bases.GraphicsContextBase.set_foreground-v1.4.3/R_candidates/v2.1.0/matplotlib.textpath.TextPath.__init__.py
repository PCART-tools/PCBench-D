    def __init__(self, xy, s, size=None, prop=None,
                 _interpolation_steps=1, usetex=False,
                 *kl, **kwargs):
        """
        Create a path from the text. No support for TeX yet. Note that
        it simply is a path, not an artist. You need to use the
        PathPatch (or other artists) to draw this path onto the
        canvas.

        xy : position of the text.
        s : text
        size : font size
        prop : font property
        """

        if prop is None:
            prop = FontProperties()

        if size is None:
            size = prop.get_size_in_points()

        self._xy = xy
        self.set_size(size)

        self._cached_vertices = None

        self._vertices, self._codes = self.text_get_vertices_codes(
                                            prop, s,
                                            usetex=usetex)

        self._should_simplify = False
        self._simplify_threshold = rcParams['path.simplify_threshold']
        self._has_nonfinite = False
        self._interpolation_steps = _interpolation_steps
