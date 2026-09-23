  def __repr__(self):
    # Override the repr so that the metadata attached to the lowered op does not
    # contain unstable function ids. This plays more nicely with computation
    # fingerprint calculation in the compilation cache.
    return f'_ArgMinMaxReducer({self._value_comparator.__name__})'
