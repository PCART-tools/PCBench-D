def _get_figure_keywords():
    bp = import_required('bokeh.plotting', _BOKEH_MISSING_MSG)
    o = bp.Figure.properties()
    o.add('tools')
    return o
