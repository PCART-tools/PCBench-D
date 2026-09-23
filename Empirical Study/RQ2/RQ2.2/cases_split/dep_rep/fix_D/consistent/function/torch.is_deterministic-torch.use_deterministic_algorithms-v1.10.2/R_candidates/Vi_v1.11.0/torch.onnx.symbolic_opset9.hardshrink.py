@parse_args("v", "f")
def hardshrink(g, self, lambd):
    lambd_op = g.op("Constant", value_t=torch.FloatTensor([lambd]))
    cond = logical_or(g, gt(g, self, lambd_op), lt(g, self, neg(g, lambd_op)))
    return g.op("Where", cond, self, g.op("Constant", value_t=torch.FloatTensor([0])))
