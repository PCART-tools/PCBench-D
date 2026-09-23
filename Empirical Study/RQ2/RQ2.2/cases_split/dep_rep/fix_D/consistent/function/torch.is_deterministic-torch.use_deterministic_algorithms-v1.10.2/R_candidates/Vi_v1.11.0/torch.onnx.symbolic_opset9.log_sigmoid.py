@parse_args("v")
def log_sigmoid(g, input):
    p = g.op("Sigmoid", input)
    return g.op("Log", p)
