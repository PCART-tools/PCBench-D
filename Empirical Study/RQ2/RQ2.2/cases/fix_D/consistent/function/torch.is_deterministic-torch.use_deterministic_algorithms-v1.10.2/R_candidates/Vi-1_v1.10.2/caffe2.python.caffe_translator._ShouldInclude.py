def _ShouldInclude(net_state, layer):
    """A function that reproduces Caffe's inclusion and exclusion rule."""
    ret = (len(layer.include) == 0)
    # check exclude rules: if any exclusion is met, we shouldn't include.
    ret &= not any([_StateMeetsRule(net_state, rule) for rule in layer.exclude])
    if len(layer.include):
        # check include rules: if any inclusion is met, we should include.
        ret |= any([_StateMeetsRule(net_state, rule) for rule in layer.include])
    return ret
