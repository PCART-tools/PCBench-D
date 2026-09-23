@parse_args("v")
def hardswish(g, self):
    return g.op("HardSwish", self)
