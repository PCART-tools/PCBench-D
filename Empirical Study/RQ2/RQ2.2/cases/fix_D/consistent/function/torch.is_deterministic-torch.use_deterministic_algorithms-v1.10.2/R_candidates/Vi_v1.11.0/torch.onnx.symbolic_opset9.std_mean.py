def std_mean(g, input, *args):
    var, mean = var_mean(g, input, *args)
    return g.op("Sqrt", var), mean
