@symbolic_helper.parse_args("v", "is", "i", "i")
def _var_mean(g: jit_utils.GraphContext, input, dim, correction, keepdim):
    return symbolic_helper._var_mean_helper(g, input, dim, correction, keepdim)
