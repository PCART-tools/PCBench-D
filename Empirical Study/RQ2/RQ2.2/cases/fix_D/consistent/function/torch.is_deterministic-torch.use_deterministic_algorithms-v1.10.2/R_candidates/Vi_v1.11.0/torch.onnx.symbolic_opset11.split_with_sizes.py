@parse_args("v", "v", "i", "i")
def split_with_sizes(g, self, split_sizes, dim, _outputs=None):
    return split(g, self, split_sizes, dim, _outputs)
