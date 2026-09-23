def is_compatible(candidate_range, assignment, static_blobs):
    (name, range_) = assignment[-1]
    if name in static_blobs:
        return False
    if candidate_range.defined is None or range_.defined is None \
      or range_.used is None:
        return False
    return candidate_range.defined > range_.used
