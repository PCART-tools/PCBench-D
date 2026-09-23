@parse_args("v", "f", "f")
def hardtanh(g, self, min_val, max_val):
    return g.op("Clip", self, min_f=min_val, max_f=max_val)
