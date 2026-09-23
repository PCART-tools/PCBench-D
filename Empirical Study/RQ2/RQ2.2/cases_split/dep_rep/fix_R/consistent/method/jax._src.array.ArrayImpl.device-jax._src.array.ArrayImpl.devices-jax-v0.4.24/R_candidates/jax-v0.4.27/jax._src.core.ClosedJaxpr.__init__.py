  def __init__(self, jaxpr: Jaxpr, consts: Sequence):
    assert len(consts) == len(jaxpr.constvars)
    # assert not any(isinstance(c, Tracer) for c in consts)  # TODO(mattjj): enable
    self._jaxpr = jaxpr
    self._consts = list(consts)
