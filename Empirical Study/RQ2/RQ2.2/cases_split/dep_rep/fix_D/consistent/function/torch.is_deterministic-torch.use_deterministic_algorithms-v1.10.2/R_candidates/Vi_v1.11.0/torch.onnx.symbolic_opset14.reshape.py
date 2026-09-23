@parse_args("v", "v")
def reshape(g, self, shape):
    return sym_help._reshape_helper(g, self, shape)
