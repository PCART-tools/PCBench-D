def _cast_func_template(to_i, g, input, non_blocking):
    return g.op("Cast", input, to_i=to_i)
