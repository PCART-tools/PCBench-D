def std(g, input, *args):
    var, _ = var_mean(g, input, *args)
    return g.op("Sqrt", var)
