@_api.deprecated("3.6", alternative="a vendored copy of _tick_update_position")
def tick_update_position(tick, tickxs, tickys, labelpos):
    """Update tick line and label position and style."""
    _tick_update_position(tick, tickxs, tickys, labelpos)
