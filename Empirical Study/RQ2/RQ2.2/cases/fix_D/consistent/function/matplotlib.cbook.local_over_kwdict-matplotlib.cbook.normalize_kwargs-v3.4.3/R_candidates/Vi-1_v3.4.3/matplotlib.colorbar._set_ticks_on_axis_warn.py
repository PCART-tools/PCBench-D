def _set_ticks_on_axis_warn(*args, **kw):
    # a top level function which gets put in at the axes'
    # set_xticks and set_yticks by ColorbarBase.__init__.
    _api.warn_external("Use the colorbar set_ticks() method instead.")
