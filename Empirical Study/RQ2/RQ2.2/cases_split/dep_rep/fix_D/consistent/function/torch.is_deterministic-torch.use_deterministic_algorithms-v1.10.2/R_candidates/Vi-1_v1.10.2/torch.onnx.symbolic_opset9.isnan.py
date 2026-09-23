@parse_args("v")
def isnan(g, input):
    output = g.op("IsNaN", input)
    return output
