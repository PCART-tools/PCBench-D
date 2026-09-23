@parse_args('v', 'i')
def one_hot(g, self, num_classes):
    values = g.op("Constant", value_t=torch.LongTensor([0, 1]))
    depth = g.op("Constant", value_t=torch.LongTensor([num_classes]))
    return g.op("OneHot", self, depth, values, axis_i=-1)
