def _apply_style(d, warn=True):
    mpl.rcParams.update(_remove_blacklisted_style_params(d, warn=warn))
