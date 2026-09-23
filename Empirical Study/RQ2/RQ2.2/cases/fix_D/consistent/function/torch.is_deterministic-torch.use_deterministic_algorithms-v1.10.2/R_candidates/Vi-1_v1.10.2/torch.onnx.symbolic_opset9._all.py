def _all(g, input):
    return g.op("Not", _any(g, g.op("Not", input)))
