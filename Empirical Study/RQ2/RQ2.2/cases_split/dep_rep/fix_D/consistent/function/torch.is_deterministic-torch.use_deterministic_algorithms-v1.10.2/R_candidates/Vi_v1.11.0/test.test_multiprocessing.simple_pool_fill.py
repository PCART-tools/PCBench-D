def simple_pool_fill(tensor):
    tensor.fill_(4)
    return tensor.add(1)
