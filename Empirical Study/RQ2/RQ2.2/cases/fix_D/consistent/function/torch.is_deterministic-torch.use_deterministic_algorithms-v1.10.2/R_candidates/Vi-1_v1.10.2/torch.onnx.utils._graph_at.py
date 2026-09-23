def _graph_at(g, opname, *args, **kwargs):
    return g.op("ATen", *args, operator_s=opname, **kwargs)
