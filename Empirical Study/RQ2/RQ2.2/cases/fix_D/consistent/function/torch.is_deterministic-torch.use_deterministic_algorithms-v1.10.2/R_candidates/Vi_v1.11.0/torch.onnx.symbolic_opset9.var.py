def var(g, input, *args):
    var, _ = var_mean(g, input, *args)
    return var
