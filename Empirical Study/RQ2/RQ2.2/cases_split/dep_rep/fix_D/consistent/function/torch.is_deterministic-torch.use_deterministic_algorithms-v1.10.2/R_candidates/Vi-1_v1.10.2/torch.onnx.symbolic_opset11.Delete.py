def Delete(g, tensor_list, dim):
    return g.op("SequenceErase", tensor_list, dim)
