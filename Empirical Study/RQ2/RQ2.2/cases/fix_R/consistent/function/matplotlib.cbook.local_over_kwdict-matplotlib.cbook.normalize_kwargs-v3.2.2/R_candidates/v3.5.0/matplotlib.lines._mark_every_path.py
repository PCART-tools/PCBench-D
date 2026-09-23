def _mark_every_path(markevery, tpath, affine, ax):
    """
    Helper function that sorts out how to deal the input
    `markevery` and returns the points where markers should be drawn.

    Takes in the `markevery` value and the line path and returns the
    sub-sampled path.
    """
    # pull out the two bits of data we want from the path
    codes, verts = tpath.codes, tpath.vertices

    def _slice_or_none(in_v, slc):
        """Helper function to cope with `codes` being an ndarray or `None`."""
        if in_v is None:
            return None
        return in_v[slc]

    # if just an int, assume starting at 0 and make a tuple
    if isinstance(markevery, Integral):
        markevery = (0, markevery)
    # if just a float, assume starting at 0.0 and make a tuple
    elif isinstance(markevery, Real):
        markevery = (0.0, markevery)

    if isinstance(markevery, tuple):
        if len(markevery) != 2:
            raise ValueError('`markevery` is a tuple but its len is not 2; '
                             'markevery={}'.format(markevery))
        start, step = markevery
        # if step is an int, old behavior
        if isinstance(step, Integral):
            # tuple of 2 int is for backwards compatibility,
            if not isinstance(start, Integral):
                raise ValueError(
                    '`markevery` is a tuple with len 2 and second element is '
                    'an int, but the first element is not an int; markevery={}'
                    .format(markevery))
            # just return, we are done here

            return Path(verts[slice(start, None, step)],
                        _slice_or_none(codes, slice(start, None, step)))

        elif isinstance(step, Real):
            if not isinstance(start, Real):
                raise ValueError(
                    '`markevery` is a tuple with len 2 and second element is '
                    'a float, but the first element is not a float or an int; '
                    'markevery={}'.format(markevery))
            if ax is None:
                raise ValueError(
                    "markevery is specified relative to the axes size, but "
                    "the line does not have a Axes as parent")
            # calc cumulative distance along path (in display coords):
            disp_coords = affine.transform(tpath.vertices)
            delta = np.empty((len(disp_coords), 2))
            delta[0, :] = 0
            delta[1:, :] = disp_coords[1:, :] - disp_coords[:-1, :]
            delta = np.hypot(*delta.T).cumsum()
            # calc distance between markers along path based on the axes
            # bounding box diagonal being a distance of unity:
            (x0, y0), (x1, y1) = ax.transAxes.transform([[0, 0], [1, 1]])
            scale = np.hypot(x1 - x0, y1 - y0)
            marker_delta = np.arange(start * scale, delta[-1], step * scale)
            # find closest actual data point that is closest to
            # the theoretical distance along the path:
            inds = np.abs(delta[np.newaxis, :] - marker_delta[:, np.newaxis])
            inds = inds.argmin(axis=1)
            inds = np.unique(inds)
            # return, we are done here
            return Path(verts[inds], _slice_or_none(codes, inds))
        else:
            raise ValueError(
                f"markevery={markevery!r} is a tuple with len 2, but its "
                f"second element is not an int or a float")

    elif isinstance(markevery, slice):
        # mazol tov, it's already a slice, just return
        return Path(verts[markevery], _slice_or_none(codes, markevery))

    elif np.iterable(markevery):
        # fancy indexing
        try:
            return Path(verts[markevery], _slice_or_none(codes, markevery))
        except (ValueError, IndexError) as err:
            raise ValueError(
                f"markevery={markevery!r} is iterable but not a valid numpy "
                f"fancy index") from err
    else:
        raise ValueError(f"markevery={markevery!r} is not a recognized value")
