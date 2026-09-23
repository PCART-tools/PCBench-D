def get_pos_and_bbox(ax, renderer):
    """
    Get the position and the bbox for the axes.

    Parameters
    ----------
    ax
    renderer

    Returns
    -------
    pos : Bbox
        Position in figure coordinates.
    bbox : Bbox
        Tight bounding box in figure coordinates.

    """
    fig = ax.figure
    pos = ax.get_position(original=True)
    # pos is in panel co-ords, but we need in figure for the layout
    pos = pos.transformed(fig.transSubfigure - fig.transFigure)
    try:
        tightbbox = ax.get_tightbbox(renderer=renderer, for_layout_only=True)
    except TypeError:
        tightbbox = ax.get_tightbbox(renderer=renderer)

    if tightbbox is None:
        bbox = pos
    else:
        bbox = tightbbox.transformed(fig.transFigure.inverted())
    return pos, bbox
