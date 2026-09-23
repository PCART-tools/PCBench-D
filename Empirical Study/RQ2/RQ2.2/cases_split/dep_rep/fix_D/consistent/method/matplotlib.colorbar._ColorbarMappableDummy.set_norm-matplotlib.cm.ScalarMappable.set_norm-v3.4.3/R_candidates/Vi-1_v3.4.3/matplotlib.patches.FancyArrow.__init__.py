    @docstring.dedent_interpd
    def __init__(self, x, y, dx, dy, width=0.001, length_includes_head=False,
                 head_width=None, head_length=None, shape='full', overhang=0,
                 head_starts_at_zero=False, **kwargs):
        """
        Parameters
        ----------
        width : float, default: 0.001
            Width of full arrow tail.

        length_includes_head : bool, default: False
            True if head is to be counted in calculating the length.

        head_width : float or None, default: 3*width
            Total width of the full arrow head.

        head_length : float or None, default: 1.5*head_width
            Length of arrow head.

        shape : {'full', 'left', 'right'}, default: 'full'
            Draw the left-half, right-half, or full arrow.

        overhang : float, default: 0
            Fraction that the arrow is swept back (0 overhang means
            triangular shape). Can be negative or greater than one.

        head_starts_at_zero : bool, default: False
            If True, the head starts being drawn at coordinate 0
            instead of ending at coordinate 0.

        **kwargs
            `.Patch` properties:

            %(Patch_kwdoc)s
        """
        if head_width is None:
            head_width = 3 * width
        if head_length is None:
            head_length = 1.5 * head_width

        distance = np.hypot(dx, dy)

        if length_includes_head:
            length = distance
        else:
            length = distance + head_length
        if not length:
            verts = np.empty([0, 2])  # display nothing if empty
        else:
            # start by drawing horizontal arrow, point at (0, 0)
            hw, hl, hs, lw = head_width, head_length, overhang, width
            left_half_arrow = np.array([
                [0.0, 0.0],                 # tip
                [-hl, -hw / 2],             # leftmost
                [-hl * (1 - hs), -lw / 2],  # meets stem
                [-length, -lw / 2],         # bottom left
                [-length, 0],
            ])
            # if we're not including the head, shift up by head length
            if not length_includes_head:
                left_half_arrow += [head_length, 0]
            # if the head starts at 0, shift up by another head length
            if head_starts_at_zero:
                left_half_arrow += [head_length / 2, 0]
            # figure out the shape, and complete accordingly
            if shape == 'left':
                coords = left_half_arrow
            else:
                right_half_arrow = left_half_arrow * [1, -1]
                if shape == 'right':
                    coords = right_half_arrow
                elif shape == 'full':
                    # The half-arrows contain the midpoint of the stem,
                    # which we can omit from the full arrow. Including it
                    # twice caused a problem with xpdf.
                    coords = np.concatenate([left_half_arrow[:-1],
                                             right_half_arrow[-2::-1]])
                else:
                    raise ValueError("Got unknown shape: %s" % shape)
            if distance != 0:
                cx = dx / distance
                sx = dy / distance
            else:
                # Account for division by zero
                cx, sx = 0, 1
            M = [[cx, sx], [-sx, cx]]
            verts = np.dot(coords, M) + (x + dx, y + dy)

        super().__init__(verts, closed=True, **kwargs)
