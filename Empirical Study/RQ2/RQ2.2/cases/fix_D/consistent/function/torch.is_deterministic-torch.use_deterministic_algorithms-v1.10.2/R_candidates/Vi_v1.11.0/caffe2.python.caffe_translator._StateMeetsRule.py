def _StateMeetsRule(state, rule):
    """A function that reproduces Caffe's StateMeetsRule functionality."""
    if rule.HasField('phase') and rule.phase != state.phase:
        return False
    if rule.HasField('min_level') and state.level < rule.min_level:
        return False
    if rule.HasField('max_level') and state.level > rule.max_level:
        return False
    curr_stages = set(list(state.stage))
    # all stages in rule.stages should be in, otherwise it's not a match.
    if len(rule.stage) and any([s not in curr_stages for s in rule.stage]):
        return False
    # none of the stage in rule.stages should be in, otherwise it's not a match.
    if len(rule.not_stage) and any([s in curr_stages for s in rule.not_stage]):
        return False
    # If none of the nonmatch happens, return True.
    return True
