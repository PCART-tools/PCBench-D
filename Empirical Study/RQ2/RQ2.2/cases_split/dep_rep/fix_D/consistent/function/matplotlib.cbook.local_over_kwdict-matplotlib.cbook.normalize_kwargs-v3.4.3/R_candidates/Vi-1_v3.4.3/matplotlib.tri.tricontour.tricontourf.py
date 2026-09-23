@docstring.Substitution(func='tricontourf', type='regions')
@docstring.dedent_interpd
def tricontourf(ax, *args, **kwargs):
    """
    %(_tricontour_doc)s

    hatches : list[str], optional
        A list of cross hatch patterns to use on the filled areas.
        If None, no hatching will be added to the contour.
        Hatching is supported in the PostScript, PDF, SVG and Agg
        backends only.

    Notes
    -----
    `.tricontourf` fills intervals that are closed at the top; that is, for
    boundaries *z1* and *z2*, the filled region is::

        z1 < Z <= z2

    except for the lowest interval, which is closed on both sides (i.e. it
    includes the lowest value).
    """
    kwargs['filled'] = True
    return TriContourSet(ax, *args, **kwargs)
