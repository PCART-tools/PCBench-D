def _policy_from_bool(b):
    # For backward compatability
    return CheckpointPolicy.MUST_SAVE if b else CheckpointPolicy.PREFER_RECOMPUTE
