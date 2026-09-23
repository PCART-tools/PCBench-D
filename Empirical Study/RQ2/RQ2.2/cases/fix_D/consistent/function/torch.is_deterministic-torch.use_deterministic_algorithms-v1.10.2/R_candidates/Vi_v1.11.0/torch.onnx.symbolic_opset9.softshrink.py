@parse_args("v", "f")
def softshrink(g, self, lambd):
    lambd_op = g.op("Constant", value_t=torch.FloatTensor([lambd]))
    gt_cond = gt(g, self, lambd_op)
    gt_out = g.op("Where", gt_cond, sub(g, self, lambd_op), g.op("Constant", value_t=torch.FloatTensor([0])))
    lt_cond = lt(g, self, neg(g, lambd_op))
    lt_out = g.op("Where", lt_cond, add(g, self, lambd_op), g.op("Constant", value_t=torch.FloatTensor([0])))
    return add(g, gt_out, lt_out)
