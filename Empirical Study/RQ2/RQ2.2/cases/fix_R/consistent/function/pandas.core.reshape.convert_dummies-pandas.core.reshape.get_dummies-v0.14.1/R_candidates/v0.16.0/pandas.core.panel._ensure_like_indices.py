def _ensure_like_indices(time, panels):
    """
    Makes sure that time and panels are conformable
    """
    n_time = len(time)
    n_panel = len(panels)
    u_panels = np.unique(panels)  # this sorts!
    u_time = np.unique(time)
    if len(u_time) == n_time:
        time = np.tile(u_time, len(u_panels))
    if len(u_panels) == n_panel:
        panels = np.repeat(u_panels, len(u_time))
    return time, panels
