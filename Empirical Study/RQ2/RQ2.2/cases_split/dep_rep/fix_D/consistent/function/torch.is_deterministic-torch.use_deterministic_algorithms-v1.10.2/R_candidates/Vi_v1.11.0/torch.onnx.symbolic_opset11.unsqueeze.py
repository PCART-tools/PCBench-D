@parse_args("v", "i")
def unsqueeze(g, self, dim):
    return sym_help._unsqueeze_helper(g, self, [dim])
