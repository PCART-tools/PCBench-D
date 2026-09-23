@docstring.Substitution(_make_axes_param_doc, _make_axes_other_param_doc)
def make_axes_gridspec(parent, *, location=None, orientation=None,
                       fraction=0.15, shrink=1.0, aspect=20, **kw):
    """
    Create a `~.SubplotBase` suitable for a colorbar.

    The axes is placed in the figure of the *parent* axes, by resizing and
    repositioning *parent*.

    This function is similar to `.make_axes`. Primary differences are

    - `.make_axes_gridspec` should only be used with a `.SubplotBase` parent.

    - `.make_axes` creates an `~.axes.Axes`; `.make_axes_gridspec` creates a
      `.SubplotBase`.

    - `.make_axes` updates the position of the parent.  `.make_axes_gridspec`
      replaces the ``grid_spec`` attribute of the parent with a new one.

    While this function is meant to be compatible with `.make_axes`,
    there could be some minor differences.

    Parameters
    ----------
    parent : `~.axes.Axes`
        The Axes to use as parent for placing the colorbar.
    %s

    Returns
    -------
    cax : `~.axes.SubplotBase`
        The child axes.
    kw : dict
        The reduced keyword dictionary to be passed when creating the colorbar
        instance.

    Other Parameters
    ----------------
    %s
    """

    loc_settings = _normalize_location_orientation(location, orientation)
    kw['orientation'] = loc_settings['orientation']
    location = kw['ticklocation'] = loc_settings['location']

    anchor = kw.pop('anchor', loc_settings['anchor'])
    panchor = kw.pop('panchor', loc_settings['panchor'])
    pad = kw.pop('pad', loc_settings["pad"])
    wh_space = 2 * pad / (1 - pad)

    if location in ('left', 'right'):
        # for shrinking
        height_ratios = [
                (1-anchor[1])*(1-shrink), shrink, anchor[1]*(1-shrink)]

        if location == 'left':
            gs = parent.get_subplotspec().subgridspec(
                    1, 2, wspace=wh_space,
                    width_ratios=[fraction, 1-fraction-pad])
            ss_main = gs[1]
            ss_cb = gs[0].subgridspec(
                    3, 1, hspace=0, height_ratios=height_ratios)[1]
        else:
            gs = parent.get_subplotspec().subgridspec(
                    1, 2, wspace=wh_space,
                    width_ratios=[1-fraction-pad, fraction])
            ss_main = gs[0]
            ss_cb = gs[1].subgridspec(
                    3, 1, hspace=0, height_ratios=height_ratios)[1]
    else:
        # for shrinking
        width_ratios = [
                anchor[0]*(1-shrink), shrink, (1-anchor[0])*(1-shrink)]

        if location == 'bottom':
            gs = parent.get_subplotspec().subgridspec(
                    2, 1, hspace=wh_space,
                    height_ratios=[1-fraction-pad, fraction])
            ss_main = gs[0]
            ss_cb = gs[1].subgridspec(
                    1, 3, wspace=0, width_ratios=width_ratios)[1]
            aspect = 1 / aspect
        else:
            gs = parent.get_subplotspec().subgridspec(
                    2, 1, hspace=wh_space,
                    height_ratios=[fraction, 1-fraction-pad])
            ss_main = gs[1]
            ss_cb = gs[0].subgridspec(
                    1, 3, wspace=0, width_ratios=width_ratios)[1]
            aspect = 1 / aspect

    parent.set_subplotspec(ss_main)
    parent.set_anchor(loc_settings["panchor"])

    fig = parent.get_figure()
    cax = fig.add_subplot(ss_cb, label="<colorbar>")
    cax.set_aspect(aspect, anchor=loc_settings["anchor"], adjustable='box')
    return cax, kw
