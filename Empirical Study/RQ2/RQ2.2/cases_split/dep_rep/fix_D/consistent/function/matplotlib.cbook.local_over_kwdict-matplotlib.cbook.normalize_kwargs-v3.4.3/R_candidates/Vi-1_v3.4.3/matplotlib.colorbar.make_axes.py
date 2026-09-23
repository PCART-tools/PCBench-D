@docstring.Substitution(_make_axes_param_doc, _make_axes_other_param_doc)
def make_axes(parents, location=None, orientation=None, fraction=0.15,
              shrink=1.0, aspect=20, **kw):
    """
    Create an `~.axes.Axes` suitable for a colorbar.

    The axes is placed in the figure of the *parents* axes, by resizing and
    repositioning *parents*.

    Parameters
    ----------
    parents : `~.axes.Axes` or list of `~.axes.Axes`
        The Axes to use as parents for placing the colorbar.
    %s

    Returns
    -------
    cax : `~.axes.Axes`
        The child axes.
    kw : dict
        The reduced keyword dictionary to be passed when creating the colorbar
        instance.

    Other Parameters
    ----------------
    %s
    """
    loc_settings = _normalize_location_orientation(location, orientation)
    # put appropriate values into the kw dict for passing back to
    # the Colorbar class
    kw['orientation'] = loc_settings['orientation']
    location = kw['ticklocation'] = loc_settings['location']

    anchor = kw.pop('anchor', loc_settings['anchor'])
    parent_anchor = kw.pop('panchor', loc_settings['panchor'])

    parents_iterable = np.iterable(parents)
    # turn parents into a list if it is not already. We do this w/ np
    # because `plt.subplots` can return an ndarray and is natural to
    # pass to `colorbar`.
    parents = np.atleast_1d(parents).ravel()
    fig = parents[0].get_figure()

    pad0 = 0.05 if fig.get_constrained_layout() else loc_settings['pad']
    pad = kw.pop('pad', pad0)

    if not all(fig is ax.get_figure() for ax in parents):
        raise ValueError('Unable to create a colorbar axes as not all '
                         'parents share the same figure.')

    # take a bounding box around all of the given axes
    parents_bbox = mtransforms.Bbox.union(
        [ax.get_position(original=True).frozen() for ax in parents])

    pb = parents_bbox
    if location in ('left', 'right'):
        if location == 'left':
            pbcb, _, pb1 = pb.splitx(fraction, fraction + pad)
        else:
            pb1, _, pbcb = pb.splitx(1 - fraction - pad, 1 - fraction)
        pbcb = pbcb.shrunk(1.0, shrink).anchored(anchor, pbcb)
    else:
        if location == 'bottom':
            pbcb, _, pb1 = pb.splity(fraction, fraction + pad)
        else:
            pb1, _, pbcb = pb.splity(1 - fraction - pad, 1 - fraction)
        pbcb = pbcb.shrunk(shrink, 1.0).anchored(anchor, pbcb)

        # define the aspect ratio in terms of y's per x rather than x's per y
        aspect = 1.0 / aspect

    # define a transform which takes us from old axes coordinates to
    # new axes coordinates
    shrinking_trans = mtransforms.BboxTransform(parents_bbox, pb1)

    # transform each of the axes in parents using the new transform
    for ax in parents:
        new_posn = shrinking_trans.transform(ax.get_position(original=True))
        new_posn = mtransforms.Bbox(new_posn)
        ax._set_position(new_posn)
        if parent_anchor is not False:
            ax.set_anchor(parent_anchor)

    cax = fig.add_axes(pbcb, label="<colorbar>")
    for a in parents:
        # tell the parent it has a colorbar
        a._colorbars += [cax]
    cax._colorbar_info = dict(
        location=location,
        parents=parents,
        shrink=shrink,
        anchor=anchor,
        panchor=parent_anchor,
        fraction=fraction,
        aspect=aspect,
        pad=pad)
    # and we need to set the aspect ratio by hand...
    cax.set_aspect(aspect, anchor=anchor, adjustable='box')

    return cax, kw
